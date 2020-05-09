# This script serves as the backend of the CRUD app. It sets up the Flask app and handles data processing when GET and REST requests are made.

# === Imports ===
from flask import Flask, request, render_template
import json

# === App ===
def create_app():
    app = Flask(__name__)

    # --- App config ---
    # Location on AWS bucket to save uploaded files
    app.config["FILE_UPLOAD"] = "files"

    # Permitted extensions
    # NOTE: The period indicating the extension, e.g. in '.csv' should not be included
    app.config["EXTENSIONS"] = ["csv"]
    assert all(['.' not in ext for ext in app.config["EXTENSIONS"]])

    # Required sensor modes
    # NOTE These MUST be in lowercase, e.g. "accelerometer"
    app.config["SENSOR_MODES"] = ["accelerometer", "gyroscope"]
    assert all(mode == mode.lower() for mode in app.config["SENSOR_MODES"])

    # File parameters
    with open("file_parameters.json", mode='r') as fp:
        app.config["PARAMETERS"] = json.load(fp)

    # Timeout for each function
    # TODO Currently unimplemented
    app.config["FUNCTION_TIMEOUT"] = 5 

    return app


application = create_app()

# === Variables ===
# --- Variable setup ---
def reset_headers(app):
    """
    Instantiates headers based on app.config["PARAMETERS"]
    """
    return [p["description"] for p in app.config["PARAMETERS"].values()]


def reset_notifications():
    """Resets notifications between each page POST."""
    return []


def reset_files():
    """Resets files between each page file POST."""
    return []


def reset_sessions():
    """Resets sessions between each page file POST."""
    return []


# --- HTML variables ---
# What user input is desired
headers = reset_headers(application)

# Notifications on page
notifications = reset_notifications()

# --- Data variables ---
# Uploaded files 
files = reset_files()

# Grouped sessions
sessions = reset_sessions()

# === Routes ===
@application.route("/", methods=["GET", "POST"])
def home_page():
    """
    If POST, the posted data (file upload or parameter request) is processed. Background variables are updated.
    If GET, nothing needs to be run.
    Regardless, the HTML page is regenerated based on updated variables.
    """
    global notifications, files, sessions

    DEBUG("Request method:", str(request.method))

    # Check for the method
    if request.method == "POST":
        
        # Reset notifications each POST
        notifications = reset_notifications() 

        # Check if the POST was a file upload or parameter request
        if request.files: 

            # Data processing for file upload
            post_files(request)

        elif request.form: 

            # Data processing for parameter request
            post_form(request)
            
    elif request.method == "GET":
        # Do nothing
        True 

    # Generate HTML
    return html()


# === Notifications ===
def add_notification(status="", tag="", message=""):
    """
    Adds a notification to the global #notifications# variable.

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


# === File upload ===
def post_files(req):
    """
    Extracts uploaded files from req and groups them into sessions.

    Parameters
    ----------
    req (flask.request)

    Returns
    -------
    files ({}[])
    sessions ({}[])
    """
    # Instantiate file and sessions
    files = reset_files()
    sessions = reset_sessions()

    # Add file if not already added
    # Intended to avoid duplicates
    for upload in req.files.getlist("files"):
        
        # Check if the filename exists
        # Uploads are permitted only from the same folder
        # Thus files should not have the same filename
        if upload.filename not in [f["filename"] for f in files]:
            
            files.append(mmr_file(upload))

    # Number of uploaded files
    num_uploaded_files = len(files) 

    # Notification
    add_notification(
        "e" if num_uploaded_files == 0 else "s",
        message=" ".join([str(num_uploaded_files), " files uploaded."])
    )

    # Only proceed if files were uploaded
    if has_files(files):
        
        # Filter out files given the extension
        files = list(filter(lambda x: has_valid_extension(x["extension"], application.config["EXTENSIONS"]), files))

        # Number of filtered files
        num_filtered_files = len(files) 

        # Notification
        add_notification(
            "e" if num_filtered_files == 0 else "w" if num_filtered_files < num_uploaded_files else "s",
            message=" ".join([str(num_filtered_files), " files matching permitted extensions."])
        )

        # Only proceed if there are files that match permitted extensions
        if has_files(files):

            # Group files with the same session name
            for f in files: 
                # Check if the session exists
                s = session_exists(f, sessions)
                
                if s:
                    # Add file to existing session
                    add_file_to_session(f, s)
                else: 
                    # If a file has yet to be added, it indicates the session does not exist.
                    # Instantiate the session.
                    sessions.append(mmr_session(f))

            # Number of sessions
            num_sessions = len(sessions)

            # Notifications
            add_notification("s", message=" ".join([str(num_sessions), 'sessions identified.']))

            # Check that all sensor modes are available and filter by validity
            for s in sessions:
                validate_session_sensor_modes(s, application.config["SENSOR_MODES"])

            # Number of filtered sessions
            num_filtered_sessions = len(sessions)

            # Notifications
            add_notification(
                "e" if num_filtered_sessions == 0 else "w" if num_filtered_sessions < num_sessions else "s",
                message=" ".join([str(num_filtered_sessions), " sessions matching required sensor modes."])
            ) 

    return files, sessions


def has_files(f):
    """
    Checks if the length of f is greater than 0.
    """
    return len(f) > 0


def validate_session_sensor_modes(s, modes):
    """
    Validates that all sensor modes are present in the session
    """
    mode_check = list(map(lambda mode: mode.lower() in s["mmr_files"].keys(), modes))

    s["sensor_mode_check"] = all(mode_check)


# === Form post ===
def wrap_form():


# def post_form(req):
#     """
#     Handles the logic for form processing
#     """
#     # Get form
#     form = req.form





# === MetaMotionR dictionaaries ===
def mmr_file(upload):
    """Generates a dictionary holding the information of the MMR File uploaded."""
    filename = upload.filename

    # Get regex and match
    regex = "(.*)_.*_(\d+-\d+-\d+T\d+\.\d+\.\d+\.\d+_\w+)_([\w\s]+)_(.*)\.(.*)"
    match = re.search(regex, filename)

    assert match is not None 

    return {
        "filename": filename,
        "session_name": match.group(1),
        "session_metadata": match.group(2),
        "session_key": "_".join([match.group(1), match.group(2)]),
        "sensor_mode": match.group(3).lower(),
        "firmware_version": match.group(4),
        "extension": match.group(5),
        "contents": upload.read().decode('utf-8')
    }


def has_valid_extension(string, exts):
    """
    Checks if string is equal to any of the values in exts.
    """
    for e in exts:
        if string.lower() == e.lower():
            return True 

    return False


def mmr_session(mmr_file):
    """Generates a dictionary holding the MMR Session."""
    return {
        # Index
        "index": len(sessions) + 1,
        
        # Session info
        "session_key": mmr_file["session_key"],
        "session_name": mmr_file["session_name"],
        "session_metadata": mmr_file["session_metadata"],
        "firmware_version": mmr_file["firmware_version"],
        "mmr_files": {
            mmr_file["sensor_mode"]: mmr_file
        },

        # HTML inputs
        "inputs": [],

        # Metadata
        "sensor_mode_check": False, # Whether all sensor modes required by the program are present in this session
        "valid_inputs": False, # Check if the inputs are all valid
        "has_dataframe": False, # Check that it has a dataframe
        "dataframe": None, # Dataframe of metrics
        "metric_errors": None, # List of errors while generating metrics

        # "validated": False,
        # "saved": False,
        # "dataframe": None
    }


def session_exists(f, sessions):
    """Checks if the session for f already exists."""
    for s in sessions:
        if s["session_key"] == f["session_key"]:
            return s 

    return False 


def add_file_to_session(f, s):
    """
    Adds file f to session s.
    """
    s["mmr_files"][f["sensor_mode"]] = f


# === Debug ===
def DEBUG(*arg):
    print("DEBUG", *arg)