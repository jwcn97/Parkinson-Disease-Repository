"""
app.py 

This serves as the backend machine of the CRUD application. 
This script sets up the Flask app and handles the data processing logic when GET and POST requests are made.
"""

# === Imports ===
import json
import pandas as pd
 
from flask import Flask, request, render_template
from mmr import MMRFile, MMRSession, MMRSessionParam, MMRSessionParamList
from io import StringIO

import jing_wei_function_test as jwf

# === App === 
app = Flask(__name__)

# --- Application configurations ---
# Location on AWS bucket to save uploaded files
app.config["FILE_UPLOAD"] = "files"

# Permitted extensions
app.config["FILE_EXTENSIONS"] = [".csv"]

# Required sensor modes
# These MUST be in lowercase
# e.g. "accelerometer", "gyroscope", "euler"
app.config["SENSOR_MODES"] = ["accelerometer", "gyroscope"]

assert all(mode == mode.lower() for mode in app.config["SENSOR_MODES"]), "All the SENSOR_MODE values must be in lowercase."

# File parameters
fp = open("file_parameters_config.json")
app.config["PARAMETERS"] = json.load(fp)
fp.close()

# Functions to be run
app.config["FUNCTIONS"] = [
    # jwf.main.overall_main
]

# === Variables ===
# Notifications
notifications = []

# MMRFile objects
files = []

# MMRSession objects
sessions = []

# MMRSessionParamList
mmr_spl = None

# === GET/POST logic === 
@app.route('/', methods=["GET", "POST"])
def home():
    """
    Handles the logic that occurs whenever the home page is accessed/refreshed.

    The logic is split based on the request method.
    If the method is a POST, the posted data is processed.
    If the method is a GET, nothing changes. 
    Regardless, the HTML page is re-generated based on updated variables.
    """

    # Check for the method
    if request.method == "POST": 
        # Reset notifications each POST
        reset_notifications()

        # Check if the POST was a file upload or parameter check
        if request.files: 
            # TODO Data processing for file upload
            post_request_files(request)

        elif request.form:
            # TODO Data processing for form submission
            post_request_form(request)

    elif request.method == "GET":
        # Nothing
        True

    # Generate page HTML
    return html()


# === Data processing ===
def post_request_files(request):
    """Instantiates the global #files# variable using the given FileStorage objects.
    The File() objects are then mapped into MMRFile() objects.
    The global #sessions# variable is instantiated with MMRSession() objects, from the list of MMRFile() objects.

    Parameters
    ----------
    request: (Flask request)
    """
    # Accesses global #files# and #sessions# variables
    global files, sessions, mmr_spl

    # Reset both files, sessions, and mmr_spl
    reset_files()
    reset_sessions()
    reset_mmr_spl()

    # # Add to #files# if the filename doesn't exist
    # # To avoid duplicates 
    # for upload in fs: 
    #     if upload.filename not in [f.filename for f in files]:
    #         files.append(upload)
    files = request.files.getlist("files")

    # Instantiate MMRFile objects
    files = [MMRFile(x) for x in files]
    num_uploaded_files = len(files)

    # Notification for number of files uploaded
    if num_uploaded_files == 0:
        # If there are no files, throw an error.
        add_notification("e", message=' '.join([str(num_uploaded_files), 'files uploaded.']))
    else:
        add_notification("s", message=' '.join([str(num_uploaded_files), 'files uploaded.']))
        
        # Only proceed if files were uploaded
        # We filter files out given the extension
        files = list(filter(lambda x: x.extension in app.config["FILE_EXTENSIONS"], files))

        # Notification for number of files matching permitted extensions.
        status = "s"
        if len(files) == 0:
            status = "e"
        elif len(files) < num_uploaded_files:
            status = "w"

        add_notification(status, message=' '.join([str(len(files)), "files matching permitted extensions"]))

        # Only proceed if there are files matching permitted extensions
        if len(files) > 0:
            sessions = group_files_into_sessions(files)

            # Update notification
            add_notification("s", message=" ".join([str(len(sessions)), 'sessions identified.']))

            # Check that all sensor modes are available
            for s in sessions:
                s.validate_sensor_modes(app.config["SENSOR_MODES"])

            # Filter out unvalidated sessions
            num_identified_sessions = len(sessions)
            sessions = list(filter(lambda s: s.valid_session == True, sessions))

            # Notifications
            status = "s"
            if len(sessions) == 0:
                status = "e"
            elif len(sessions) != num_identified_sessions:
                status = "w"

            add_notification(status, message=" ".join([str(len(sessions)), "sessions matching required sensor types."]))

            # Instantiate each MMRSessionParam object and add it to #mmr_spl#
            mmr_spl = instantiate_mmr_spl(mmr_spl, sessions)


def reset_files():
    """Resets the #files# variable
    """
    global files 

    files = []


def reset_sessions():
    """Resets the #sessions# variable
    """
    global sessions

    sessions = []


def reset_mmr_spl():
    """Resets the #mmr_spl# variable.
    """
    global mmr_spl
       
    mmr_spl = MMRSessionParamList(
        [
            {"id": k, "description": v["description"]} for k, v in app.config["PARAMETERS"].items()
        ]
    )


def group_files_into_sessions(files):
    """Groups the files into sessions based on their session_key and returns it. 
    """
    sessions = []

    for f in files:
        # Boolean to indicate if a file has been added
        file_added = False 

        # Loop through existing sessions to check if a session with the same session key exists
        for s in sessions:
            if s.session_key == f.session_key:
                s.add_mmr_file(f)

                file_added = True
                
                break 

        # If a file has yet to be added, it indicates the session does not exist.
        # Instantiate the session.
        if not file_added:
            sessions.append(MMRSession(f))

    return sessions


def instantiate_mmr_spl(mmr_spl, sessions):
    """Instantiates #mmr_spl# and returns it.
    """
    # Recompile app.config["PARAMETERS"] for MMRSessionParam
    parameters = []

    for k, v in app.config["PARAMETERS"].items():
        parameters.append({
            "id": k,
            "values": v["values"]
        })

    # Instantiate each MMRSessionParam object and add it to #mmr_spl#
    for sx, s in enumerate(sessions):
        param = MMRSessionParam(s, sx, parameters)

        mmr_spl.add_session_param(param)

    return mmr_spl

def post_request_form(request):
    """Uses MMRSessionParamList to verify the inputs given.
    """
    # TODO
    valid_mmr_indices = mmr_spl.validate_inputs(request.form)

    for mmr_param in valid_mmr_indices:
        # TODO
        # Save
        print("Save:", sessions[mmr_param.index].session_key)

        # Sets the dataframe for the session
        sessions[mmr_param.index].set_dataframe(get_metric(sessions[mmr_param.index]))

    True 


def get_metric(session):
    """Gets the metric dataframe for the desired session
    """
    # Accelerometer dataframe
    accel_df = pd.read_csv(StringIO(session.sensor_modes["accelerometer"].file))

    # Gyroscope dataframe
    gyro_df = pd.read_csv(StringIO(session.sensor_modes["gyroscope"].file))

    # # Reset streams
    # session.sensor_modes["accelerometer"].file.stream().seek(0)
    # session.sensor_modes["gyroscope"].file.stream().seek(0)

    # Instantiate JSON
    json = {
        "filename": session.session_key,
        "name": session.session_key, 
        # The same as filename was previously the full name of the file
        # However, it made little sense to represent 'sessions' by the name of the files of one of their sensor modes
        "saved_name": session.session_name,
        "metadata": session.session_metadata,
        "accelerometer": None,
        "gyroscope": None,
        "accel_df": accel_df,
        "gyro_df": gyro_df,
        "version": session.firmware_version
    }

    for function in app.config["FUNCTIONS"]:
        function(copy_json(json))

    # print(json)
    
    """
     - filename: str # full name of the file, including .csv
 - name: str # sub-name of the file, all the way before 'Acelerometer/Gyroscope', basically saved_name + '_' + metadata
 - saved_name: str # the name that was input by the user when saving data on the MetaBase app
 - metadata: str # the metadata appended by the MetaBase app when saving sensor data
 - accelerometer: FileStorage # accessing this will return a 'None' to you
 - gyroscope: FileStorage # accessing this will return a 'None' to you
 - accel_df: DataFrame() # copy of the accelerometer dataframe
 - gyro_df: DataFrame() # copy of the gyroscope dataframe
 - version: str
    """


def copy_json(json):
    
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
    copied['filename'] = json['filename']
    copied['name'] = json['name']
    copied['saved_name'] = json['saved_name']
    copied['metadata'] = json['metadata']
    copied['version'] = json['version']

    # Do not include FileStorage objects
    copied['accelerometer'] = None
    copied['gyroscope'] = None

    # Add copies of dataframe
    copied['accel_df'] = json['accel_df'].copy()
    copied['gyro_df'] = json['gyro_df'].copy()

    return copied


# === HTML ===
def html():
    """Generates the page HTML.
    
    Displays any notifications as a result of GET/POST requests.

    If #sessions# exists, a parameter request form is generated.
    For each session in #sessions#, a dataframe of metrics is also generated.
    These dataframes, when shown, also indicate when the data is not saved as per the parameter request forms. 

    Returns
    -------
    html (str)
    """
    # TODO
    # Page HTML
    html = ""

    # Header
    html += render_template("header.html")

    # Upload bar
    html += render_template("upload_bar.html")

    # Notifications
    if notifications:
        html += '<hr>'
        html += render_template(
            "notifications.html",
            notifications=notifications
        )

    # Parameter request
    if mmr_spl is not None and len(mmr_spl.session_params) > 0:
        html += '<hr>'
        html += render_template(
            "parameter_request.html",
            headers=mmr_spl.headers,
            params=mmr_spl.session_params
        )

    return html 


def reset_notifications():
    """Resets the global #notifications# variable.
    """
    # Access the global variable
    global notifications

    # Reset
    notifications = []


def add_notification(status="", tag="", message=""):
    """Adds a notification to the global #notifications# variable.

    Parameters
    ----------
    status (str)
        Whether the action is a "success", "warning", or "error". 
        Also accepts "s", "w", and "e" respectively.
        Any other values are rejected.
    tag (str)
        The content of the tag, e.g. "[INFO]", "[ERROR]", etc.
    message (str)
        The message associated with the notification.
    """
    # Access the global #notifications# variable
    global notifications

    # Run through permitted values of #status#
    if status.lower() == "success" or status.lower() == "s":
        color = "green"

        if not tag: 
            tag = "[SUCCESS]"        
    elif status.lower() == "warning" or status.lower() == "w":
        color = "orange"
        
        if not tag: 
            tag = "[WARNING]"
    elif status.lower() == "error" or status.lower() == "e":
        color = "red"

        if not tag: 
            tag = "[ERROR]"
    else:
        color = ""

    # Append to global variable #notifications#
    notifications.append({
        "color": color,
        "tag": tag,
        "message": message
    })