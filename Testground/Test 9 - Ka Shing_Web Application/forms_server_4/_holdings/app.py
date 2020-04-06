# === Imports ===
import re

from flask import Flask, render_template, request, redirect
from page_html import Home
 
from mmr import MMRFile, MMRSession
from exceptions import UnsupportedNameFormatException 

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

# Requested inputs
app.config["INPUTS"] = [
    {
        "id": "test_type",
        "description": "Test type",
        "legals": ["ftap"]
    },
    {
        "id": "test_location",
        "description": "Test location",
        "legals": ["forearm", "wrist"]
    },
    {
        "id": "severity",
        "description": "Severity level",
        "legals": ["lvl0", "lvl1", "lvl2", "lvl3", "lvl4"]
    }
]

# === Variables === 
# HTML page object
page = Home(app.config["INPUTS"])

# Dataframe to hold file metrics
dataframe = None 

# Files
files = [] # Files that were uploaded
sessions = [] # Sessions grouped together from the uploaded files

# raw_files = [] # Files that were uploaded
# filtered_files = [] # Files that match the given extensions.
# grouped_files = [] # Files grouped together based on their metadata.
# queued_files = [] # Files that were uploaded but unsaved

# === HTML ===
@app.route('/', methods=["GET", "POST"])
def home():
    """
    Handles the logic that occurs whenever the home page is accessed/refreshed. 

    The logic is split based on the request method.
    If the method is a "POST", the function handles the data processing functions, updating variables where necessary.
    If the method is a "GET", the function generates the HTML based on the available variables.

    POST
    ----
    [TODO] Add a third method 'Refresh' or find a way to set 'sessions' on AWS. 
    There are two types of "POST" requests:

    At the start of each POST request, we reset the HTML page. It will be rebuilt during the GET logic.
    The Notification Section is rebuilt during the course of the POST logic.

        1. File upload
        --------------
            Description
            -----------
            File upload requests result in the upload of X files. 
            We filter these files for the permitted extensions as defined in app.config["FILE_EXTENSIONS"] (CSV)
            We then group the remaining extensions into 'sessions'. 
            We then filter these sessions based on the desired sensor modes (accelerometer, gyroscope, etc.)

            Variables
            ---------
            The list of files uploaded is updated here. 
            Thus, we clear/overwite the files uploaded whenever this is run.            
            
        2. Data forms  
        -------------
            Description
            -----------
            Data form requests result in the submission of essentially X by Y information. 
            Here, X is the number of sessions. Y is the number of parameters per session, e.g. 'test type', 'location', etc.
            Each parameter 'Y' is checked as to whether it's legal. 
            If they are all legal, we save the sessions and generate their dataframes.
            The ones that are not legal will require a fix to their values. 

            Variables
            ---------
            Each file's dataframe is uploaded here. 
            We don't overwrite existing dataframes; we just add them to the dictionaries. 

    GET
    ---
    The GET response depends on the available parameters.

    The Upload Section is always present. 
    The Notification Section is populated during the POST logic.

    GET/POST
    --------
    The Data Form Section is populated based on the uploaded files that have not been saved, i.e. they do not have dataframes.
        (The Data Form Section should show, grayed out, the sessions that were successfully submitted.)
    The Metric Display Section is populated during the GET logic based on the availability of the metric dataframes. 
    """
    # Access global variables
    global page, dataframe, files, sessions

    # Reload the webpage's elements
    page.reload()

    # Check for the method
    if request.method == "POST":

        # Check if the POST request was a file upload or data request
        if request.files:
            # Extract uploaded files
            files = page.post_files(request) 

            # Instantiate File class
            files = list(map(lambda x: MMRFile(x), files))

            # Notification for number of files uploaded
            page.update_notification(success='success', msg=' '.join([str(len(files)), ' files uploaded.']))
            
            # We filter out the files given the extension
            for f in files:
                f.has_extension(app.config["FILE_EXTENSIONS"])

            validated_files = sum([f.valid_extension for f in files])
            extension_check = 'success'
            if validated_files == 0:
                extension_check = 'error'
            elif validated_files != len(files):
                extension_check = 'warning'

            page.update_notification(success=extension_check, msg=' '.join([str(validated_files), ' files matching permitted extensions.']))

            # Only proceed if we have validated files
            if validated_files != 0:
                # Reset sessions
                sessions = []

                # We extract file metadata for those with the correct extensions
                # We then group them into sessions
                for f in files:
                    if f.valid_extension:
                        # Extract file metadata
                        try: 
                            f.extract_metadata_from_filename()
                        except UnsupportedNameFormatException: 
                            # [TODO] Support for future potential unsupported name formats
                            True

                        # Group into sessions
                        # Check if a session already exists
                        # If it exists, append it to that session instead
                        # Otherwise, add it to the array of sessions
                        s = MMRSession(f)
                        
                        if s.session_name in [i.session_name for i in sessions]:
                            for i in sessions:
                                if s.session_name == i.session_name:
                                    i.add_file(f)

                                    break
                        else:
                            sessions.append(s)

                # print('files:', files, 'sessions:', sessions, end='\n')
                page.update_notification(success='success', msg=' '.join([str(len(sessions)), ' sessions identified.']))

                # Check that all sensor types in the session are accounted for
                for s in sessions:
                    s.validate_sensor_modes(app.config["FILE_TYPES"])

                validated_sessions = sum([s.valid_session for s in sessions])
                session_check = 'success'
                if validated_sessions == 0:
                    session_check = 'error'
                elif validated_sessions != len(sessions):
                    session_check = 'warning'

                page.update_notification(success=session_check, msg=' '.join([str(validated_sessions), ' sessions matching desired sensor types.']))

        elif request.form:
            # Get saved names
            session_form_data = page.post_form(request)

            print(session_form_data)

            # Check for legality of data
            for k, v in session_form_data.items():
                # k is the index corresponding to the index of of our sessions in #sessions# variable
                # v is a list of dictionaries with the fields "test_id" and "test_value"
                # "test_id" corresponds to "id" in app.config["INPUTS"]
                for vx in v:
                    for i in app.config["INPUTS"]:
                        if vx["test_id"] == i["id"]:
                            # We found the INPUT id
                            # Test for legality
                            
                
                'test'

    elif request.method == "GET":
        True

    # Check for the need for data request forms
    # We loop through each session
    # But only if it is a valid session
    for sx, s in enumerate(list(filter(lambda x: x.valid_session, sessions))):

            # We attempt to extract the default values for each desired 'input'
            defaults = []

            for inputs in app.config["INPUTS"]:
                match = ''
                saved_name = s.saved_name.split('-')

                # Strip every string in saved_name
                saved_name = [s.strip() for s in saved_name]

                # Using the legal values of each input, 
                # We run through the saved user name and attempt to extract a match
                # [TODO] Write a program to ensure all legal values do not have overlaps
                for legal_value in inputs["legals"]:
                    if legal_value.strip() in saved_name:
                        match = legal_value
                        break 

                defaults.append({
                    "id": '-'.join([str(sx), inputs["id"]]),
                    "default": match
                })
                
            # We update the data requests for this particular session
            # page.update_data_requests(s.session_name, index=sx, add_info=list(s.mmr_files.keys()), defaults=defaults)
            page.update_data_requests(sx, s.session_name, descriptions=list(s.mmr_files.keys()), inputs=defaults)

    return page.render()



    # """
    # Handles the logic that occurs whenever the home page is accessed/refreshed. 
    
    # System state
    # ----------------------
    # We show the upload input.
    # If there are qeued files, we display the data request forms. 
    # Else if there is a dataframe, we display the metrics dataframe. 
    # Options: 
    #     1. Upload one/more file(s) and submit
    #         If there are queued files, we give a warning.
    #         Otherwise, we submit the files. 
    #     2. Refresh
    #         If there are qeueud files, we give a warning.
    #         Otherwise, we refresh the page, dropping the queued files. 
    #         There is no overriding the dataframe, so it is still shown. 
    #     3. (Data request form) Submit with no information
    #         The submission is not permitted. 
    #     4. (Data request form) Submit with partial information
    #         If the application mode is 'strict', the submission is not permitted.
    #         If the application mode is 'lenient', we save and remove the appropriate files from the queued files. 
    #         If there are still queued files, we resend the data request forms. 
    #         Else, we set the dataframe. 
    #     5. (Data request form) Submit with complete information
    #         We save and remove the appropriate files. 
    #         We set the dataframe. 
    # """
    # Global variables
    # global dataframe, raw_files, filtered_files, grouped_files, queued_files

    # print(dataframe, raw_files, filtered_files, grouped_files, queued_files)

    # Check for the type of request
    # If it's a GET request, the page itself is requested
    #   We follow the logic in the finalised state system
    #       The upload bar will be shown
    #       If there are qeueud files, the data request forms will be shown
    #       Else if there is a data frame, it will be shown
    # If it's a POST request, something was submitted
    #   We upload the queued files and reload for a GET response to follow the above logic
    # if request.method == "GET":
    #     # Full HTML element to return
    #     full_html = ''

    #     # HTML head element
    #     html_head = bh('head', content=render_template('head.html'))

    #     # HTML upload element
    #     html_upload = bh('div', content=render_template('upload.html'))

    #     # HTML body
    #     html_body = bh('body', content=html_upload)
    #     html_body += '<hr>'

    #     # Check if any files were uploaded
    #     if len(raw_files) > 0:
    #         # HTML files uploaded
    #         html_body += bn('success', '[SUCCESS]', str(len(raw_files)) + ' ' + __plural(raw_files, 'file', 'files') + ' uploaded.')

    #         # [TODO] Function for notification
    #         # HTML filtered files
    #         notification_type = 'success'
    #         notification_value = '[SUCCESS]'
    #         if len(filtered_files) == 0: 
    #             notification_type = 'error'
    #             notification_value = '[ERROR]'
    #         elif len(filtered_files) != len(raw_files):
    #             notification_type = 'warning'
    #             notification_value = '[WARNING]'

    #         html_body += bn(notification_type, notification_value, str(len(filtered_files)) + ' ' +  __plural(filtered_files, 'file', 'files') + ' matching permitted extensions.')

    #         # Only continue if there are files
    #         if len(filtered_files) > 0: 
    #             # HTML for file groups
    #             html_body += bn('success', '[SUCCESS]', str(len(grouped_files)) + ' ' + __plural(grouped_files, 'session', 'sessions') + ' identified.')

    #             # HTML for queued groups
    #             notification_type = 'success'
    #             notification_value = '[SUCCESS]'
    #             if len(queued_files) == 0: 
    #                 notification_type = 'error'
    #                 notification_value = '[ERROR]'
    #             elif len(queued_files) != len(grouped_files):
    #                 notification_type = 'warning'
    #                 notification_value = '[WARNING]'
                
    #             html_body += bn(notification_type, notification_value, str(len(queued_files)) + ' ' + __plural(queued_files, 'session', 'sessions') + ' matching desired data types.')

    #             # Only continue if there are queued files
    #             if len(queued_files) > 0:
    #                 html_body += '<hr>'

    #                 html_table_contents = ''
                    
    #                 # Table header
    #                 html_table_contents += render_template('data_request_header.html')



    #                 # html_body += bh('table', content=''.join([
                        
    #                 # ]))
                    
    #                 # For each qeueud file
    #                 for ix, i in enumerate(queued_files):
    #                     saved_name = i['saved_name']

    #                     parameters = extract_test_parameters(saved_name)

    #                     html_table_contents += render_template(
    #                         'data_request.html',
    #                         row_number=str(ix + 1),
    #                         session_name=i['session_name'],
    #                         metadata=i['metadata'],
    #                         description=', '.join([modes for modes in i['modes'].keys()]),
    #                         type=parameters['test'],
    #                         location=parameters['location'],
    #                         level=parameters['level'],
    #                         code=parameters['code']
    #                     )

    #                 html_table_contents = bh('table', content=html_table_contents)

    #                 html_body += bh('form', 
    #                 attr={'action':'/', 'method': "POST", 'name':'data-request-form'},
    #                 content=''.join([
    #                     html_table_contents,
    #                     render_template('data_request_submit.html')
    #                 ]))

    #                 #  + [
    #                 #     render_template('data_request.html', row_number=str(ix), index=str(ix + 1), session_name=i['session_name'], description=', '.join([j for j in i['modes']])) for ix, i in enumerate(queued_files)
    #                 # ]))
                

    #     # Check if there are pending files
    #     if len(queued_files) > 0: 

    #         # [TODO] HTML files in queue display

    #         # [TODO] For each file, display data request forms

    #         True
    #     elif dataframe is not None:
    #         # [TODO] HTML table for dataframe

    #         True
            
    #     full_html = html_head + html_body

    #     return full_html

    # elif request.method == "POST":
    #     # [TODO] Add files to queued_files

    #     # We check that there are files to be added to the queue
    #     # If there are no files, we do nothing
    #     if request.files: 
    #         # [TODO] There are files to be added to the queue
    #         # Extract uploaded files
    #         raw_files = request.files.getlist("files")
            
    #         # [TODO] Ensure that none of them are 'False'
    #         # print(raw_files[0])

    #         # We filter out the files given the extensions
    #         filtered_files = filter_file_extensions(raw_files, app.config["FILE_EXTENSIONS"])

    #         # We extract the files' parameters
    #         grouped_files = []
    #         for file in filtered_files:
    #             grouped_files.append(extract_file_parameters(file))

    #         grouped_files = group(grouped_files)

    #         # We filter the grouped files based on the desired data modes, ala 'file types'
    #         queued_files = list(filter(lambda x: all([i in x['modes'].keys() for i in app.config["FILE_TYPES"]]), grouped_files))

    #         True

    #         # We overwrite all arrays other than queued_files to save memory
    #         raw_files = range(len(raw_files))

    #     # We check that, otherwise, a data request form has been submitted
    #     if request.form:
    #         for ix, i in enumerate(queued_files):
    #             i['form_data'] = {
    #                 'type': request.form.get("type-" + str(ix + 1)),
    #                 'location': request.form.get("location-" + str(ix + 1)),
    #                 'level': request.form.get("level-" + str(ix + 1)),
    #                 'code': request.form.get("code-" + str(ix + 1))
    #             }

    #         for ix, i in enumerate(reversed(queued_files)):
    #             print(i['form_data'])

    #     else: 
    #         # There are no files to be added to the queue
    #         # Do nothing
    #         True

    #     return redirect('/')


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
    files (File()[])
        Files to be filtered
    extensions (str[])
        An array of permissible extensions

    Returns
    -------
    filtered (FileStorage[])
        The files that end with the given extensions
    """
    for f in files:
        # Set the 'show' attribute to False 
        # Set it to True if it matches any extension
        f.show = False 

        for e in extensions:
            if f.filename.endswith(e):
                f.show = True
                
    return files


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
                },
                'mode_check': False
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
