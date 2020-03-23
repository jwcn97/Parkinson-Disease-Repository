# === Imports ===
import re

from flask import Flask, render_template, request, redirect
from build_html import build_html as bh
from build_html import build_notification as bn

# === App ===
app = Flask(__name__)

application = app # For AWS to locate the app

# --- Application configurations ---
# Location on AWS bucket to save uploaded files
app.config["FILE_UPLOAD"] = 'files' 

# Permitted extensions
app.config["FILE_EXTENSIONS"] = ['.csv'] 

# Permitted types of data, as per the lowercase of what meta
# These MUST be in lowercase
# e.g. "accelerometer", "gyroscope", "euler"
# These will also be used as keys to the file dictionaries
app.config["FILE_TYPES"] = ["accelerometer", "gyroscope"]

# Types of tests
app.config["TEST_TYPES"] = ['ftap']

# Location of tests
app.config["TEST_LOCATIONS"] = ["forearm", "wrist"]

# File names regex
# Regex sections
# 	1: Name, as given by whoever is using the Metawear app
#	2: Metadata, as given by the app
#	3: Type of data, e.g. Accelerometer, gyroscope
#	4: (Most likely) firmware version of the sensors
#	5: File extension
app.config["FILE_NAME_REGEX"] = "(.*)_.*_(\d+-\d+-\d+T\d+\.\d+\.\d+\.\d+_\w+)_([\w\s]+)_(.*)\.(.*)"

# === Variables ===
# Dataframe to hold file metrics
dataframe = None 

# Files
raw_files = [] # Files that were uploaded
filtered_files = [] # Files that match the given extensions.
grouped_files = [] # Files grouped together based on their metadata.
queued_files = [] # Files that were uploaded but unsaved

# === HTML ===
@app.route('/', methods=["GET", "POST"])
def home():
    """
    Handles the logic that occurs whenever the home page is accessed/refreshed. 
    
    ((The following is a discussion of the system states. The finalised system state can be found below.))
    System states
    -------------
    STATE 1: UPLOAD
        Contains the upload input
        If there is a dataframe, show the dataframe
        Options: 
            1. Upload one file and submit
                Proceed to STATE 2
            2. Upload multiple files and submit
                Proceed to STATE 2
            3. Refresh the page
                Reload to STATE 1
                Retain the dataframe

    STATE 2: DATA REQUEST
        Contains the upload input
        Contains the data request forms
        Options: 
            1. Upload one file and submit
                Give warning on data loss; proceed to STATE 2
            2. Upload multiple files and submit
                Give warning on data loss; proceed to STATE 2
            3. Refresh
                Give warning on data loss; proceed to STATE 1
                Retain the previous dataframe. 
            4. Submit with no information
                Refuse submission
            5. Submit with partial information
                If 'strict', refuse.
                Else if 'lenient', save the appropriate information and request the remainder.
                    Go to STATE 2. 
            6. Submit with complete information
                Save the information. 
                Set dataframe and go to STATE 1 with dataframe enabled. 

    We notice STATE 1 and STATE 2 can be combined. 
    In both cases, we show the upload input. 
    If there are queued files, we return the data request forms. 
    Else if there are no queued files, we check for the dataframe metric. 
    
    For the options, 1 2 and 3 can give warning on data loss if there are queued files. Otherwise, they perform their actions. 
    Options 4, 5 and 6 are handled if there are files queued. 

    Finalised system state
    ----------------------
    We show the upload input.
    If there are qeued files, we display the data request forms. 
    Else if there is a dataframe, we display the metrics dataframe. 
    Options: 
        1. Upload one/more file(s) and submit
            If there are queued files, we give a warning.
            Otherwise, we submit the files. 
        2. Refresh
            If there are qeueud files, we give a warning.
            Otherwise, we refresh the page, dropping the queued files. 
            There is no overriding the dataframe, so it is still shown. 
        3. (Data request form) Submit with no information
            The submission is not permitted. 
        4. (Data request form) Submit with partial information
            If the application mode is 'strict', the submission is not permitted.
            If the application mode is 'lenient', we save and remove the appropriate files from the queued files. 
            If there are still queued files, we resend the data request forms. 
            Else, we set the dataframe. 
        5. (Data request form) Submit with complete information
            We save and remove the appropriate files. 
            We set the dataframe. 
    """
    # Global variables
    global dataframe, raw_files, filtered_files, grouped_files, queued_files

    print(dataframe, raw_files, filtered_files, grouped_files, queued_files)

    # Check for the type of request
    # If it's a GET request, the page itself is requested
    #   We follow the logic in the finalised state system
    #       The upload bar will be shown
    #       If there are qeueud files, the data request forms will be shown
    #       Else if there is a data frame, it will be shown
    # If it's a POST request, something was submitted
    #   We upload the queued files and reload for a GET response to follow the above logic
    if request.method == "GET":
        # Full HTML element to return
        full_html = ''

        # HTML head element
        html_head = bh('head', content=render_template('head.html'))

        # HTML upload element
        html_upload = bh('div', content=render_template('upload.html'))

        # HTML body
        html_body = bh('body', content=html_upload)
        html_body += '<hr>'

        # Check if any files were uploaded
        if len(raw_files) > 0:
            # HTML files uploaded
            html_body += bn('success', '[SUCCESS]', str(len(raw_files)) + ' ' + __plural(raw_files, 'file', 'files') + ' uploaded.')

            # [TODO] Function for notification
            # HTML filtered files
            notification_type = 'success'
            notification_value = '[SUCCESS]'
            if len(filtered_files) == 0: 
                notification_type = 'error'
                notification_value = '[ERROR]'
            elif len(filtered_files) != len(raw_files):
                notification_type = 'warning'
                notification_value = '[WARNING]'

            html_body += bn(notification_type, notification_value, str(len(filtered_files)) + ' ' +  __plural(filtered_files, 'file', 'files') + ' matching permitted extensions.')

            # Only continue if there are files
            if len(filtered_files) > 0: 
                # HTML for file groups
                html_body += bn('success', '[SUCCESS]', str(len(grouped_files)) + ' ' + __plural(grouped_files, 'session', 'sessions') + ' identified.')

                # HTML for queued groups
                notification_type = 'success'
                notification_value = '[SUCCESS]'
                if len(queued_files) == 0: 
                    notification_type = 'error'
                    notification_value = '[ERROR]'
                elif len(queued_files) != len(grouped_files):
                    notification_type = 'warning'
                    notification_value = '[WARNING]'
                
                html_body += bn(notification_type, notification_value, str(len(queued_files)) + ' ' + __plural(queued_files, 'session', 'sessions') + ' matching desired data types.')

                # Only continue if there are queued files
                if len(queued_files) > 0:
                    html_body += '<hr>'

                    html_table_contents = ''
                    
                    # Table header
                    html_table_contents += render_template('data_request_header.html')



                    # html_body += bh('table', content=''.join([
                        
                    # ]))
                    
                    # For each qeueud file
                    for ix, i in enumerate(queued_files):
                        saved_name = i['saved_name']

                        parameters = extract_test_parameters(saved_name)

                        html_table_contents += render_template(
                            'data_request.html',
                            row_number=str(ix + 1),
                            session_name=i['session_name'],
                            metadata=i['metadata'],
                            description=', '.join([modes for modes in i['modes'].keys()]),
                            type=parameters['test'],
                            location=parameters['location'],
                            level=parameters['level'],
                            code=parameters['code']
                        )

                    html_table_contents = bh('table', content=html_table_contents)

                    html_body += bh('form', content=''.join([
                        html_table_contents,
                        render_template('data_request_submit.html')
                    ]))

                    #  + [
                    #     render_template('data_request.html', row_number=str(ix), index=str(ix + 1), session_name=i['session_name'], description=', '.join([j for j in i['modes']])) for ix, i in enumerate(queued_files)
                    # ]))
                

        # Check if there are pending files
        if len(queued_files) > 0: 

            # [TODO] HTML files in queue display

            # [TODO] For each file, display data request forms

            True
        elif dataframe is not None:
            # [TODO] HTML table for dataframe

            True
            
        full_html = html_head + html_body

        return full_html

    elif request.method == "POST":
        # [TODO] Add files to queued_files

        # We check that there are files to be added to the queue
        # If there are no files, we do nothing
        if request.files: 
            # [TODO] There are files to be added to the queue
            # Extract uploaded files
            raw_files = request.files.getlist("files")
            
            # [TODO] Ensure that none of them are 'False'
            print(raw_files[0])

            # We filter out the files given the extensions
            filtered_files = filter_file_extensions(raw_files, app.config["FILE_EXTENSIONS"])

            # We extract the files' parameters
            grouped_files = []
            for file in filtered_files:
                grouped_files.append(extract_file_parameters(file))

            grouped_files = group(grouped_files)

            # We filter the grouped files based on the desired data modes, ala 'file types'
            queued_files = list(filter(lambda x: all([i in x['modes'].keys() for i in app.config["FILE_TYPES"]]), grouped_files))

            True

            # We overwrite all arrays other than queued_files to save memory
            raw_files = range(len(raw_files))

        else: 
            # There are no files to be added to the queue
            # Do nothing
            True

        return redirect('/')


def __plural(array, single='', plural='s'):
    """
    Simple function to return either the single or the plural given the length of the array.

    Parameters
    ----------
    array ([])
        Array to check if the plural form of a noun should be returned. 
    single (str)
        By convention, returns ''. Can be replaced to return the entire single noun if they differ greatly. 
    plural (str)
        By convention, returns 's'. Can be replaced to return the entire noun if it differs greatly. 

    Returns
    -------
    (boolean)
        If arr is single, returns single. Else, returns plural.
    """
    if len(array) == 1:
        return single
    else:
        return plural


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


def extract_file_parameters(file):
    """
    Extracts the parameters of the given file. 
    Each file will have its 'saved name', 'metadata', 'data mode', and 'file extension' saved. 
    
    Parameters
    ----------
    file (FileStorage)

    Returns
    -------
    result (dictionary, {})
        Key-value pairs:
            'session_name' (str): The complete name of the sensor, given by 'saved_name' + 'metadata'
            'saved_name' (str): The name as saved by the user
            'metadata' (str): The name as saved by the sensor
            'mode' (str): The type of data, e.g. accelerometer. This is automatically in lowercase. 
            'extension' (str): The file extension. 
            'version' (str): The version of the sensor during the time of measurement.
            'file' (FileStorage): The original file. 
    """
    # Get the regex
    regex = re.search(app.config["FILE_NAME_REGEX"], file.filename)

    # [TODO] Handle the case where the regex potentially failed

    # Collect regex groups
    saved = regex.group(1)
    metadata = regex.group(2)
    mode = regex.group(3)
    version = regex.group(4)
    extension = regex.group(5)

    # Get complete filename
    filename = '_'.join([saved, metadata])

    result = {
        'session_name': filename,
        'saved_name': saved,
        'metadata': metadata,
        'mode': mode.lower(),
        'version': version,
        'extension': extension,
        'file': file
    }

    return result


def group(dictionaries):
    """
    Groups the file dictionaries based on their shared 'session_name's
    These files will have the same 'saved_name', 'metadata', and 'version', which will be extracted to the outer dictionary.

    Parameters
    ----------
    dictionaries (dictionary[], {}[])
        Array of individual file dictionaries.

    Returns
    -------
    result (dictionary[], {}[])
        Dictionary array, where each dictionary has the following key-value pair
            'session_name' (str): Name of the session
            'saved_name' (str): Name of the saved file given by the user
            'metadata' (str): Metadata as saved by the sensor
            'version' (str): Sensor version during time of measurement
            'modes' (str): {}   
                Returns a dictionary, where the key-value pair refers to the mode in question and its corresponding dictionary.
                    'accelerometer': Returns the accelerometer file dictionary.
                    'gyroscope': Returns the gyroscope file dictionary. 
                    Not all entries are available in 'mode', depending on which files were uploaded. 
    """
    result = []

    for dictionary in dictionaries:
        # Collect existing filenames
        existing_filenames = [t['session_name'] for t in result]

        # Check if the entry exists
        # If it exists, we search for it and add the mode
        # If it doesn't exist, we instantiate it
        if dictionary['session_name'] in existing_filenames:
            # Loop through each
            for ix, i in enumerate(result):
                if i['session_name'] == dictionary['session_name']:
                    # Assert the data mode does not already exist
                    # [TODO] What if it already exists? How could it?
                    assert dictionary['mode'] not in i['modes'].keys()

                    # Add the data type to the mode
                    result[ix]['modes'][dictionary['mode']] = dictionary

                    break 
        
        else:
            # It's not in the entries yet
            result.append({
                'session_name': dictionary['session_name'],
                'saved_name': dictionary['saved_name'],
                'metadata': dictionary['metadata'],
                'version': dictionary['version'],
                'modes': {
                    dictionary['mode']: dictionary
                }
            })

    return result


def extract_test_parameters(name):
    """
    Extracts the test parameters from the given name.

    Parameters
    ----------
    name (str)
        The saved name of the file.

    Returns
    -------
    (dictionary, {})
        The result as key-value pairs  
            'test' (str): Test type
            'location' (str): Location of test
            'level' (int): Severity level
    """
    # We first split name by '-' and strip it of leading/trailing whitespace
    name = name.split('-')
    name = [t.strip() for t in name]

    # We check for the level
    name, level = find_and_pop(name, 'lvl', False)
    
    # Level could be 'None'
    if level:
        try: 
            level = int(level.replace('lvl', ''))
        except ValueError:
            level = ''
    else:
        level = ''

    # Get test type
    test = None
    for t in app.config["TEST_TYPES"]:
        name, test = find_and_pop(name, t)

        # For each test, if we find the test, we break
        if test: 
            break 
    
    # To avoid the value being 'None'
    if not test:
        test = ''

    # Get location
    location = None
    for l in app.config["TEST_LOCATIONS"]:
        name, location = find_and_pop(name, l)

        # For each location, if we find the location, we break
        if location:
            break 

    # To avoid the value being 'None'
    if not location:
        location = ''

    # [TODO] PATIENT CODE
    code = ''

    return {
        'test': test,
        'location': location,
        'level': level,
        'code': code
    }


def find_and_pop(arr, target, strict=True):
    """
    Finds the target within the array and pops it.

    Parameters
    ----------
    arr (list, [])
        The array to be searched
    target (str)
        The item to be found
    
    Returns
    -------
    arr (list, []) 
        The array with the target value popped out
    result (str)
        The target. None if it cannot be found. 
    """
    result = None 

    for ix, i in enumerate(arr):
        if strict: 
            if target == i:
                result = arr.pop(ix)

                break
        else:
            if target in i:
                result = arr.pop(ix)

                break

    return arr, result
