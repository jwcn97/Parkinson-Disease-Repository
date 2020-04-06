# This script runs all tests for app.py.

# TODO Check that PARAMETERS is reset for any test that requires it to be. 
# TODO CHeck that app.config is reset for any test that changes any part of it.

# === Imports ===
import app as my_app
import json
import pytest

from .common_functions import io_functions as iof 
from .common_functions import mmr_functions as mmrf 

# === Tests ===
# --- App ---
@pytest.fixture
def app():
    """
    Creates the app.
    """
    app = my_app.app
    return app 


def test_home_page(client):
    """
    Tests whether we can reach the home page.
    """
    # response = client.get("/")
    response = client.get("/")
    
    assert response.status_code == 200


# --- Notifications ---
def test_reset_notifications():
    my_app.reset_notifications()

    assert my_app.notifications == []


def test_add_notifications():
    # TODO More tests required
    test_variables = [
        {
            "status": "e",
            "message": " ".join(["0", 'files uploaded.']),
            "answer": {
                "color": "red",
                "message": "0 files uploaded.",
                "tag": "[ERROR]"
            }
        }, 
        {
            "status": "s",
            "message": " ".join(["17", 'files uploaded.']),
            "answer": {
                "color": "green",
                "message": "17 files uploaded.",
                "tag": "[SUCCESS]"
            }
        }, 
        {
            "status": "w",
            "message": " ".join(["17", 'files uploaded.']),
            "answer": {
                "color": "orange",
                "message": "17 files uploaded.",
                "tag": "[WARNING]"
            }
        }
    ]

    for test in test_variables: 
        my_app.add_notification(test["status"], message=test["message"])
        
        assert my_app.notifications[-1] == test["answer"]


# --- Data processing ---
def test_reset_files():
    my_app.reset_files()

    assert my_app.files == []


def test_reset_sessions():
    my_app.reset_sessions()

    assert my_app.sessions == []


def test_check_files_uploaded():
    test_variables = [
        {
            "files": [], 
            "answer": False 
        }, 
        {
            "files": [1, 2, 3],
            "answer": True 
        }
    ]

    for test in test_variables:
        my_app.files = test["files"]
        
        assert my_app.check_files() == test["answer"]


def test_filter_files_by_extension():
    # TODO More in-depth check than simply length of filtered files?
    test_variables = [
        {
            "extensions": ["txt"],
            "total": 14
        },
        {
            "extensions": ["csv"],
            "total": 10
        },
        {
            "extensions": ["txt", "csv"],
            "total": 24
        }
    ]

    # Load CSV Files
    files = iof.load_csv_files()

    # Run through tests
    for test in test_variables:

        # Instantiate my_app.files 
        my_app.files = mmrf.instantiate_mmr_files(files)
        
        # Replace FILE_EXTENSIONS in app.config
        my_app.app.config["FILE_EXTENSIONS"] = test["extensions"] 

        # Test 
        my_app.filter_files_by_extension()

        assert len(my_app.files) == test["total"]


def test_group_files_into_sessions():
    # TODO Check more than just the length
    test_variables = [
        {
            "extensions": ["txt"],
            "total": 6
        },
        {
            "extensions": ["csv"],
            "total": 5
        },
        {
            "extensions": ["txt", "csv"],
            "total": 11
        }
    ]
    
    # Load CSV files
    files = iof.load_csv_files()

    # Run through tests
    for test in test_variables:

        # Instantiate my_app.files
        my_app.files = mmrf.instantiate_mmr_files(files)

        # Replace FILE_EXTENSIONS
        my_app.app.config["FILE_EXTENSIONS"] = test["extensions"]

        # Filter
        my_app.filter_files_by_extension()

        # Reset sessions
        my_app.reset_sessions()

        # Test grouping
        my_app.group_files_into_sessions()

        assert len(my_app.sessions) == test["total"], len(my_app.sessions)


def test_validate_session_sensor_modes():
    # Load CSV files
    files = iof.load_csv_files()

    # Test variables
    with open("./tests/test_variables/test_app_validate_session_sensor_mode.json") as fp:
        test_variables = json.load(fp)
    
    for test in test_variables:
        # Instantiate MMRSessions
        my_app.files = mmrf.instantiate_mmr_files(files)

        # Replace SENSOR_MODES
        my_app.app.config["SENSOR_MODES"] = test["sensor_modes"]

        # Filter
        my_app.filter_files_by_extension()

        # Reset sessions
        my_app.reset_sessions()

        # Filter
        my_app.group_files_into_sessions()

        # Test validation
        my_app.validate_session_sensor_modes()

        assert sum([t["session"].valid_session for t in my_app.sessions]) == test["result"]


def test_filter_sessions_by_validity():
    # Load files
    files = iof.load_csv_files()
    
    # Test variables
    with open("./tests/test_variables/test_filter_sessions_by_validity.json") as fp:
        test_variables = json.load(fp)
    
    for test in test_variables:
        # Instantiate MMRSessions
        my_app.files = mmrf.instantiate_mmr_files(files)

        # Replace SENSOR_MODES
        my_app.app.config["SENSOR_MODES"] = test["sensor_modes"]

        # Filter
        my_app.filter_files_by_extension()

        # Reset sessions
        my_app.reset_sessions()

        # Filter
        my_app.group_files_into_sessions()

        # Validate sensors
        my_app.validate_session_sensor_modes()

        # Test filter
        my_app.filter_sessions_by_validity()

        assert [t["session"].session_key for t in my_app.sessions] == test["result"]


def test_post_form():
    assert False, "Unimplemented"


# --- HTML ---
def test_html():
    assert False, "Unimplemented"


def test_generate_parameter_requests():
    assert False, "Unimplemented"


def test_load_parameters():
    with open("file_parameters.json", "r") as fr:
        parameters = json.load(fr)

    my_app.load_parameters()

    assert my_app.app.config["PARAMETERS"] == parameters


def test_header_instantiation():
    # Test variables
    with open("./tests/test_variables/test_header_instantiation.json", "r") as fr:
        test_variables = json.load(fr) 

    for test in test_variables:
        my_app.app.config["PARAMETERS"] = {t["id"]: {"description": t["description"]} for t in test["test_var"]}

        my_app.instantiate_headers()

        assert my_app.headers == test["result"]


def test_extract_values_from_name():
    result_inputs = [
        [
            {'name': 'test_type', 'value': '', 'status': None}, 
            {'name': 'test_location', 'value': '', 'status': None}, 
            {'name': 'severity', 'value': '', 'status': None}
        ],
        [
            {'name': 'test_type', 'value': '', 'status': None}, 
            {'name': 'test_location', 'value': '', 'status': None}, 
            {'name': 'severity', 'value': '', 'status': None}
        ],
        [
            {'name': 'test_type', 'value': '', 'status': None}, 
            {'name': 'test_location', 'value': 'forearm', 'status': None}, 
            {'name': 'severity', 'value': 'lvl2', 'status': None}
        ],
        [
            {'name': 'test_type', 'value': '', 'status': None}, 
            {'name': 'test_location', 'value': 'forearm', 'status': None}, 
            {'name': 'severity', 'value': 'lvl3', 'status': None}
        ],
        [
            {'name': 'test_type', 'value': '', 'status': None}, 
            {'name': 'test_location', 'value': 'forearm', 'status': None}, 
            {'name': 'severity', 'value': 'lvl4', 'status': None}
        ]
    ]


    files = iof.load_csv_files()

    my_app.files = mmrf.instantiate_mmr_files(files)

    my_app.load_configurations()

    # Replace SENSOR_MODES
    # my_app.app.config["SENSOR_MODES"] = test["sensor_modes"]

    # Filter
    my_app.filter_files_by_extension()

    # Reset sessions
    my_app.reset_sessions()

    # Filter
    my_app.group_files_into_sessions()
    
    # Test extraction
    my_app.extract_values_from_name()

    assert [t["inputs"] for t in my_app.sessions] == result_inputs