# === Imports ===
import re
import boto3

import pandas as pd

from flask import Flask, render_template, request, redirect

from keys import ACCESS_KEY, SECRET_KEY, BUCKET

# === AWS ===
s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

# === Flask === 
app = Flask(__name__)

application = app # For AWS to locate the app

# Application configurations
app.config['FILE_UPLOAD'] = 'files' # Location on AWS bucket to save uploaded files
app.config['FILE_EXTENSIONS'] = ['.csv'] # Permitted extensions
app.config['FILE_REGEX'] = '(.*)_(Metawear_\d+-\d+-\d+T\d+\.\d+\.\d+\.\d+_\w+)_([\w\s]+)_(.*)\.(.*)' # Regex for file names
# Regex sections
# 	1: Name, as given by whoever is using the Metawear app
#	2: Metadata, as given by the app
#	3: Type of data, e.g. Accelerometer, gyroscope
#	4: (Most likely) firmware version of the sensors
#	5: File extension

# === HTML ===
@app.route('/',  methods=["GET", "POST"])
def home():
    """
    Function to handle the home page
    """
    dataframe = None # Dataframe to hold metrics

    # Check for request
    # If it is a GET, then nothing was posted
    # If it is a POST, then a file/multiple files was/were previously uploaded
    if request.method == "GET":
        # Nothing needs to be done
        True

    elif request.method == "POST":
        # Post
        # We ensure that there are files to be posted
        if request.files:

            # Extract uploaded files
            raw_files = request.files.getlist("files")

            # We filter out the files that have the given extensions
            filtered_files = filter_file_extensions(raw_files, app.config["FILE_EXTENSIONS"])

            # For the purpose of passing to the dataframe functions
            # We group the files based on their names
            # The grouped files are accessible through a dictionary
            # [TODO] Any file without an accelerometer/gyroscope pair should evoke an error
            # Any 'exceptional case' (e.g. Euler Angles) will be handled by future releases
            grouped_files = group(filtered_files)

            # Filter out the files that only have both 'accelerometer' and 'gyroscope' data
            # These files may have additional data, like 'Euler Angles' in addition to the above two
            grouped_files = list(filter(lambda x: 'accelerometer' in x.keys() and 'gyroscope' in x.keys(), grouped_files))

            # [TODO] Check if any files that were 'grouped' are not filtered from the above function

            # Save each file, while setting the 'last file' as the final file
            # The last file will be the file with its metrics displayed
            # [TODO] We want to give them a notice of which file's info is displayed
            # As well as mentioning that multiple files were uploaded but only the last file is displayed
            target_file = save_grouped_files(grouped_files)
            
            # [TODO] Display metrics
            dataframe = get_metrics(target_file)

        else:
            # There are no files; don't do anything
            True

    return build_page(dataframe)


def filter_file_extensions(files, extensions):
    """
    Filters files based on their extensions

    Parameters
    ----------
    files (FileStorage[])
        Files to be filtered
    extensions (str[])
        An array of permissible extensions

    Returns
    -------
    filtered (FileStorage[])
        The files that end with the given extensions
    """
    filtered = []

    for extension in extensions:
        filtered.extend(list(filter(lambda x: x.filename.endswith(extension), files)))

    return filtered


def group(files):
    """
    Groups files based on their names

    Parameters
    ----------
    files (FileStorage[])
        Files to be grouped
    
    Returns
    -------
    grouped ({})
        Dictionary holding information for the grouped files
    """
    grouped = []

    for file in files:
        # Get the filename
        filename = file.filename

        # Extract regex
        regex = re.search(app.config["FILE_REGEX"], filename)

        # [TODO] Handle the case where regex is potentially 'None'

        # Collect regex groups
        sensor_filename = regex.group(1)
        sensor_metadata = regex.group(2)
        sensor_datatype = regex.group(3)
        sensor_version = regex.group(4)
        sensor_extension = regex.group(5) # Unused

        # Set 'complete' filename
        complete_filename = sensor_filename + '_' + sensor_metadata

        # Set sensor type to lowercase
        sensor_datatype = sensor_datatype.lower()

        # Collect existing filenames to be compared
        existing_filenames = [t['name'] for t in grouped]
        
        # Check if the file already exists
        # If it exists, we search for it to append the FileStorage to the dictionary as an additional key-value pair
        # If it doesn't exist, we instantiate it
        if complete_filename in existing_filenames:
            # Loop through each 
            for jx, j in enumerate(grouped):
                if j['name'] == complete_filename:
                    # Assert that the sensor_datatype doesn't already exist
                    # [TODO] What if it exists? How could it?
                    assert sensor_datatype not in j.keys()

                    grouped[jx][sensor_datatype] = file 

                    break

        else:
            # It's not in the file yet
            grouped.append({
                'name': complete_filename,
                'saved_name': sensor_filename,
                'metadata': sensor_metadata,
                sensor_datatype: file,
                'version': sensor_version
            })
    
    return grouped


def save_grouped_files(files):
    """
    Saves the FileStorage in the given files

    Parameters
    ----------
    files ({}[])
        Array of dictionaries generated by the group() function

    Returns
    -------
    file ({})
        The final file in the array of dictionaries
    """
    file = None

    for file in files:
        # [TODO] Do not save if it will overwrite

        # Repeat it for accelerometer and gyroscope
        for datatype in ['accelerometer', 'gyroscope']:
            try:
                file_storage = file[datatype]

                # Ensure it's saved
                contents = file_storage.read() 

                # Reset stream
                file_storage.stream.seek(0)

                # [TODO] Save
                upload(file_storage.filename, contents)

            except Exception:
                # [TODO] What to do if there is an exception?
                True

    # print(file)

    return file


def upload(filename, contents):
    """
    Uploads a file to an S3 bucket

    Parameters
    ----------
    filename (str)
        Name of the file
    contents (str)
        Contents of the file
    """
    # s3.Object(BUCKET, app.config["FILE_UPLOAD"] + "/" + filename).put(Body=contents)
    s3.Object(BUCKET, "/".join([app.config["FILE_UPLOAD"], filename])).put(Body=contents)


def get_metrics(file):
    """
    Function to extract the metrics for the given file

    Parameters
    ----------
    file ({})
        The dictionary containing the file
    
    Returns
    -------
    dataframe (DataFrame())
        The resulting dataframe
    """
    # Parse dataframes of accelerometer and gyroscope data
    file['accel_df'] = pd.read_csv(file['accelerometer'])
    file['gyro_df'] = pd.read_csv(file['gyroscope'])

    # print(file)

    # Make a copy of the dictionary and all its contents
    file_copy = copy(file)

    # [TODO] Metrics go here

    return pd.DataFrame()

def copy(file):
    """
    Generates a copy of the JSON to be passed into the metric functions

    Parameters
    ----------
    file ({})
        The file to be copied

    Returns
    -------
    copied ({})
        The copied file
    """
    copied = {}

    # Strings are immediately copied upon assignment
    copied['name'] = file['name']
    copied['saved_name'] = file['saved_name']
    copied['metadata'] = file['metadata']
    copied['version'] = file['version']

    # Do not include FileStorage objects
    copied['accelerometer'] = None
    copied['gyroscope'] = None

    # Add copies of dataframe
    copied['accel_df'] = file['accel_df'].copy()
    copied['gyro_df'] = file['gyro_df'].copy()

    return copied


def build_page(dataframe):
    html = '<html>'

    html += '<head>'
    html += render_template('header.html')
    html += '</head>'

    html += '<body>'
    html += render_template('upload.html')
    html += '</body>'

    if dataframe is not None: 
        # [TODO] Return the dataframe as well
        True

    html += '</html>'

    # return render_template('upload.html')
    return html