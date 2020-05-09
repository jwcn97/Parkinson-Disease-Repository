# This script serves as the backend of the CRUD application. It sets up the Flask app and handles the data processing logic when GET and REST requests are made.

# === Imports ===
from flask import Flask, request, render_template
import json
import re
import pandas as pd
from io import StringIO
import math

import jing_updated.test.main as jwf

# === App ===
def create_app():
    app = Flask(__name__)

    # --- Application configurations ---
    # Location on AWS bucket to save uploaded files
    app.config["FILE_UPLOAD"] = "files"

    # Permitted extensions
    # NOTE: The period indicating the extension, e.g. in '.csv' should not be included
    app.config["EXTENSIONS"] = ["csv"]

    assert all(['.' not in ext for ext in app.config["EXTENSIONS"]])

    # Required sensor modes
    # These MUST be in lowercase
    # e.g. "accelerometer"
    app.config["SENSOR_MODES"] = ["accelerometer", "gyroscope"]

    assert all(mode == mode.lower() for mode in app.config["SENSOR_MODES"])

    # File parameters
    with open("file_parameters.json", mode='r') as fp:
        app.config["PARAMETERS"] = json.load(fp)

    # Functions to be run to get metrics    
    app.config["FUNCTIONS"] = [
        ("Jing Wei's functions", jwf.overall_main)
    ]

    # Timeout for each function
    app.config["FUNCTION_TIMEOUT"] = 5 

    return app
 
app = create_app()

application = app

# === Variables ===
headers = None # What user input is desired
notifications = None # Notifications on page
files = None # Uploaded files
sessions = None # Grouped sessions

# --- Variable setup ---
def reset_headers():
    """Instantiate headers based on app.config["PARAMETERS"]"""
    global headers

    headers = [p["description"] for p in app.config["PARAMETERS"].values()]


def reset_notifications():
    """Resets notifications between each page POST."""
    global notifications

    notifications = []


def reset_files():
    """Resets files between each page file POST."""
    global files

    files = []


def reset_sessions():
    """Resets sessions between each page file POST."""
    global sessions

    sessions = []


reset_headers()
reset_notifications()
reset_files()
reset_sessions()


# === Routes ===
@app.route("/", methods=["GET", "POST"])
def home_page():
    """
    Handles the logic that occurs when the home page is accesssed/refreshed.

    The logic is split based on the request method.
    If POST, the posted data (file upload or parameter request) is processed. Background variables are updated.
    If GET, nothing needs to be run.
    Regardless, the HTML page is regenerated based on updated variables.
    """
    print("DEBUG - Request method: " + str(request.method))

    # Check for the method
    if request.method == "POST":
        
        # Reset notifications each POST
        reset_notifications() 

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


# === Data processing ===
def post_files(request):
    """
    Instantiates the global #files# variable with the uploaded files. 

    Parameters
    ----------
    request (Flask request)
    """
    global files

    # Reset global variables
    reset_files()
    reset_sessions()

    # Add to #files# if the filename doesn't exist
    # To avoid duplicates
    for upload in request.files.getlist("files"):
        
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
    if check_files():
        
        # Filter out files given the extension
        filter_files_by_extension()

        # Number of filtered files
        num_filtered_files = len(files) 

        # Notification
        add_notification(
            "e" if num_filtered_files == 0 else "w" if num_filtered_files < num_uploaded_files else "s",
            message=" ".join([str(num_filtered_files), " files matching permitted extensions."])
        )

        # Only proceed if there are files that match permitted extensions
        if check_files():
            
            # Group files with the same session name
            group_files_into_sessions()

            # Number of sessions
            num_sessions = len(sessions)

            # Notifications
            add_notification("s", message=" ".join([str(num_sessions), 'sessions identified.']))

            # Check that all sensor modes are available
            validate_session_sensor_modes()

            # Filter out unvalidated sessions
            filter_sessions_by_validity()

            # Number of filtered sessions
            num_filtered_sessions = len(sessions)

            # Notifications
            add_notification(
                "e" if num_filtered_sessions == 0 else "w" if num_filtered_sessions < num_sessions else "s",
                message=" ".join([str(num_filtered_sessions), " sessions matching required sensor modes."])
            ) 


def check_files():
    """
    Checks if the length of #files# is more than 1.
    """
    return len(files) > 0


def filter_files_by_extension():
    """
    Filters files based on the given extensions in app.config["EXTENSIONS"]
    """
    global files 

    files = list(filter(lambda x: x["extension"] in app.config["EXTENSIONS"], files))


def group_files_into_sessions():
    """
    Groups #files# based on their session_key
    """
    global sessions 

    for f in files:
        # Boolean to indicate if a file has been added
        file_added = False 

        # Loop through existing sessions to check if a session with the same session key exists
        for s in sessions:
            if s["session_key"] == f["session_key"]:
                s["mmr_files"][f["sensor_mode"]] = f

                file_added = True
                
                break 

        # If a file has yet to be added, it indicates the session does not exist.
        # Instantiate the session.
        if not file_added:
            sessions.append(mmr_session(f))


def validate_session_sensor_modes():
    """
    Validates that all sensor modes in app.config["SENSOR_MODES"] are present in the session
    """
    for s in sessions:
        mode_check = list(map(lambda mode: mode.lower() in s["mmr_files"].keys(), app.config["SENSOR_MODES"]))

        s["sensor_mode_check"] = all(mode_check)


def filter_sessions_by_validity():
    """
    Filters sessions based on their validity
    """
    global sessions 

    sessions = list(filter(lambda s: s["sensor_mode_check"] == True, sessions))

    # Reset index of sessions
    for ix, s in enumerate(sessions): 
        s["index"] = ix + 1


def post_form(request):
    """
    Handles the logic for form posting
    """
    # We extract the requests
    forms = request.form

    validate_html_inputs(forms)
        
    # Check validity of all inputs for each session
    for s in sessions:
        if all([t["status"] for t in s["inputs"]]):
            s["valid_inputs"] = True 

            # Save
            # TODO The case where there is no dataframe but the file is saved. Separate post_form from dataframe generation?
            save_session_files(s)

    # Generate metric dataframes
    for s in sessions: 
        if s["valid_inputs"] and not s["has_dataframe"]:
            results, errors = get_metrics(s)

            # If there are errors, add it to the session
            # Set the value of session, rather than append
            if errors != []:
                s["metric_errors"] = errors

            # Check that results is not []
            if results != []:
                # Parse to dataframe
                dataframe = pd.DataFrame(results)

                # Check that dataframe is not empty
                if not dataframe.empty: 
                    # Dataframe processing
                    dataframe = process_dataframe(dataframe)
                    
                    s["has_dataframe"] = True
                    s["dataframe"] = dataframe 
                
            # TODO What do we do about s["metric_errors"]?



def validate_html_inputs(forms):
    """
    Parameters
    ----------
    forms: request.forms
    """
    for k, v in forms.items():
        key = k.rsplit("-", 1)

        test_id = key[0]
        test_index = int(key[1])
        value = v 

        # Checks if it's a valid value
        valid_value = False 

        # The test_index is the index to access from #sessions#
        # Within a session in sessions, we access the "inputs" key
        # Then, we search in all dictionaries in "inputs" to find a dictionary with the "name" being the test_id
        for ix, i in enumerate(sessions[test_index]["inputs"]):
            if i["name"] == test_id:
                # Set value
                sessions[test_index]["inputs"][ix]["value"] = value

                # Check if value is valid
                if value in app.config["PARAMETERS"][test_id]["values"]: 

                    valid_value = True 

                # Set validity of value
                sessions[test_index]["inputs"][ix]["status"] = valid_value

                break


def get_metrics(session):
    """
    Gets the metrics dataframe for the current session
    """
    # Results
    results = []
    errors = []

    for name, f in app.config["FUNCTIONS"]:
        # Generate the JSON to be passed to each metric function call    
        session_json = generate_session_json(session)
        
        # Function call
        try:
            # r = to(app.config["FUNCTION_TIMEOUT"], f, args=(session_json, ))

            r = f(session_json)

            results.extend(r)
        # except FunctionTimedOut:
        #     # TODO
        #     True
        #     print("TIMEDOUT")

        #     errors.append("Function timed out: " + str(name))
        except:
            # TODO
            True 
            print("EXCEPTION")

            errors.append("Exception occurred: " + str(name))
        
    return results, errors


def generate_session_json(session):
    """
    Generates a JSON to be passed to the metric functions.
    """
    # Load accelerometer and gyroscope dataframes
    # Accelerometer dataframe
    accelerometer_df = pd.read_csv(StringIO(session["mmr_files"]["accelerometer"]["contents"]))

    # Gyroscope dataframe
    gyroscope_df = pd.read_csv(StringIO(session["mmr_files"]["gyroscope"]["contents"]))

    # Copy accelerometer and gyroscope dataframes to avoid overwriting
    accel_df = accelerometer_df.copy()
    gyro_df = gyroscope_df.copy()

    return {
            "filename": session["session_key"],
            "name": session["session_key"], 
            # The same as filename was previously the full name of the file
            # However, it made little sense to represent 'sessions' by the name of the files of one of their sensor modes
            "saved_name": session["session_name"],
            "metadata": session["session_metadata"],
            "accelerometer": {
                "filename": session["mmr_files"]["accelerometer"]["filename"],
                "filename_without_extension": session["mmr_files"]["accelerometer"]["filename"].rsplit('.', 1)[0]
            },
            "gyroscope": {
                "filename": session["mmr_files"]["gyroscope"]["filename"],
                "filename_without_extension": session["mmr_files"]["gyroscope"]["filename"].rsplit('.', 1)[0]
            },
            "accel_df": accel_df,
            "gyro_df": gyro_df,
            "version": session["firmware_version"]
        }


def process_dataframe(df):
    """
    Processes the dataframe prior to returning to the user
    """
    def match_units(a, b):
        # Significant figures
        if type(a) == type(int(2)) or type(a) == type(float(1.0)): 
            if abs(a) > 0: 
                # print(a)
                a = round(a, -int(math.floor(math.log10(abs(a)))) + 3) # 4 s.f.
                # print(a)
                # a = round(a, -int(math.floor(math.log10(abs(a)))))
                # print(a)
                # a = round(a, -int(math.floor(math.log10(abs(a)))) - 2)
                # print(a) 

        # Check if there are units
        if str(b).strip() == '-':
            b = ''
        else:
            b = '(' + str(b) + ')'
        
        # Return
        return " ".join([str(a), str(b)]).strip()

    # Match axes with their units
    for k, v in {
        "x": "x_unit",
        "y": "y_unit",
        "z": "z_unit",
        "resultant": "resultant_unit",
    }.items():
        df[k] = df.apply(lambda row: match_units(row[k], row[v]), axis=1)
        df = df.drop([v], axis=1)

    return df


def save_session_files(session):
    # TODO
    True


# === HTML ===
def html():
    """
    Handles the generation of the page's HTML

    Displays notifications from POST requests.

    Displays parameter request forms if a session exists.

    Displays the metric dataframe if any exist. 

    Returns
    -------
    html (str)
    """
    # Page HTML
    html = ''

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
    if sessions:
        html += '<hr>'

        html += generate_parameter_requests()

    # Dataframes
    if any([s["has_dataframe"] is True for s in sessions]):
        html += '<hr>'

        html += generate_metric_dataframes()

    # Return
    return html


def generate_parameter_requests():
    """
    Generates parameter requests HTML

    Returns
    -------
    html (str)
    """
    # Validate inputs
    # Extract legal values from name
    extract_values_from_name()

    # HTML
    html = render_template(
        "parameter_request.html",
        sessions=sessions,
        headers=headers
    )

    return html


def extract_values_from_name():
    """
    Extracts values from name based on permitted values in app.config["PARAMETERS"]
    """
    for s in sessions:
        # Check if inputs is [], if not then continue
        if s["inputs"] != []:
            continue

        # Initialize a variable to hold all inputs
        session_input = []

        # Session name
        session_name = s["session_name"]

        # Split name by '-'
        session_name = session_name.split('-')

        # Loop through all required parameters
        for param_name, param_arg in app.config["PARAMETERS"].items():

            # Extract value from name 
            match = ""

            for value in param_arg["values"]: 
                for name in session_name:
                    if value == name.strip():

                        match = value

                        break 

            session_input.append({
                "name": param_name, 
                "value": match,
                "status": None
            })

        s["inputs"] = session_input


def generate_metric_dataframes():
    """
    Handles html HTML related to the dataframes.
    """
    html = ''

    html = render_template(
        "metric_df.html",
        sessions=sessions,
    )

    return html


# === MMR Dictionaries ===
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