# Runs tests for mmr.py

# === Imports ===
import os
import pytest

from .common_functions import io_functions as iof
from .common_functions import mmr_functions as mmrf

from werkzeug.datastructures import FileStorage
from mmr import MMRFile, MMRSession

# === Tests ===
# --- MMRFile ---
@pytest.mark.filterwarnings("ignore")
def test_mmr_file():
    # Load CSV files
    files = iof.load_csv_files() 

    # File name to file properties dictionary
    # TODO Include other files in csv_files folder
    test_variables = {
        "4test-100-8g-500_Metawear_2020-02-11T13.28.11.448_C5013CAC38C1_Accelerometer_1.5.0.csv": {
            "session_name": "4test-100-8g-500",
            "session_metadata": "Metawear_2020-02-11T13.28.11.448_C5013CAC38C1",
            "session_key": "4test-100-8g-500_Metawear_2020-02-11T13.28.11.448_C5013CAC38C1",
            "sensor_mode": "accelerometer",
            "firmware_version": "1.5.0",
            "extension": ".csv"
        }, 
        "4test-100-8g-500_Metawear_2020-02-11T13.28.11.448_C5013CAC38C1_Gyroscope_1.5.0.csv": {
            "session_name": "4test-100-8g-500",
            "session_metadata": "Metawear_2020-02-11T13.28.11.448_C5013CAC38C1",
            "session_key": "4test-100-8g-500_Metawear_2020-02-11T13.28.11.448_C5013CAC38C1",
            "sensor_mode": "gyroscope",
            "firmware_version": "1.5.0",
            "extension": ".csv"
        }, 
        "4test-linacc-eul-100_Metawear_2020-02-11T13.05.36.569_C5013CAC38C1_Euler Angles_1.5.0.csv": {
            "session_name": "4test-linacc-eul-100",
            "session_metadata": "Metawear_2020-02-11T13.05.36.569_C5013CAC38C1",
            "session_key": "4test-linacc-eul-100_Metawear_2020-02-11T13.05.36.569_C5013CAC38C1",
            "sensor_mode": "euler angles",
            "firmware_version": "1.5.0",
            "extension": ".csv"
        }, 
        "4test-linacc-eul-100_Metawear_2020-02-11T13.05.36.569_C5013CAC38C1_Linear Acceleration_1.5.0.csv": {
            "session_name": "4test-linacc-eul-100",
            "session_metadata": "Metawear_2020-02-11T13.05.36.569_C5013CAC38C1",
            "session_key": "4test-linacc-eul-100_Metawear_2020-02-11T13.05.36.569_C5013CAC38C1",
            "sensor_mode": "linear acceleration",
            "firmware_version": "1.5.0",
            "extension": ".csv"
        }, 
        "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1_Euler Angles_1.5.0.txt": {
            "session_name": "4test-linacc-eul-pr-100-0.99hz",
            "session_metadata": "Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "session_key": "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "sensor_mode": "euler angles",
            "firmware_version": "1.5.0",
            "extension": ".txt"
        }, 
        "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1_Linear Acceleration_1.5.0.txt": {
            "session_name": "4test-linacc-eul-pr-100-0.99hz",
            "session_metadata": "Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "session_key": "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "sensor_mode": "linear acceleration",
            "firmware_version": "1.5.0",
            "extension": ".txt"
        }, 
        "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1_Pressure_1.5.0.txt": {
            "session_name": "4test-linacc-eul-pr-100-0.99hz",
            "session_metadata": "Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "session_key": "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "sensor_mode": "pressure",
            "firmware_version": "1.5.0",
            "extension": ".txt"
        }
    }
    
    # Instantiate each MMRFile() object
    for f in files: 
        if f.rsplit("\\", 1)[0] in test_variables.keys():
            with open(f, mode="r") as fr:
                mmr_file = mmrf.instantiate_mmr_file_from_path(f)

                assert mmr_file.session_name == test_variables["session_name"]
                assert mmr_file.session_metadata == test_variables["session_metadata"]
                assert mmr_file.session_key == test_variables["session_key"]
                assert mmr_file.sensor_mode == test_variables["sensor_mode"]
                assert mmr_file.firmware_version == test_variables["firmware_version"]
                assert mmr_file.extension == test_variables["extension"]
                assert mmr_file.contents == fr.read() 


# --- MMRSession ---
def test_mmr_session(): 
    # Load CSV variables
    files = iof.load_csv_files()

    test_variables = {
        "4test-100-8g-500_Metawear_2020-02-11T13.28.11.448_C5013CAC38C1_Accelerometer_1.5.0.csv": {
            "session_name": "4test-100-8g-500",
            "session_metadata": "Metawear_2020-02-11T13.28.11.448_C5013CAC38C1",
            "session_key": "4test-100-8g-500_Metawear_2020-02-11T13.28.11.448_C5013CAC38C1",
            "sensor_mode": "accelerometer",
            "firmware_version": "1.5.0",
        }, 
        "4test-100-8g-500_Metawear_2020-02-11T13.28.11.448_C5013CAC38C1_Gyroscope_1.5.0.csv": {
            "session_name": "4test-100-8g-500",
            "session_metadata": "Metawear_2020-02-11T13.28.11.448_C5013CAC38C1",
            "session_key": "4test-100-8g-500_Metawear_2020-02-11T13.28.11.448_C5013CAC38C1",
            "sensor_mode": "gyroscope",
            "firmware_version": "1.5.0",
        }, 
        "4test-linacc-eul-100_Metawear_2020-02-11T13.05.36.569_C5013CAC38C1_Euler Angles_1.5.0.csv": {
            "session_name": "4test-linacc-eul-100",
            "session_metadata": "Metawear_2020-02-11T13.05.36.569_C5013CAC38C1",
            "session_key": "4test-linacc-eul-100_Metawear_2020-02-11T13.05.36.569_C5013CAC38C1",
            "sensor_mode": "euler angles",
            "firmware_version": "1.5.0",
        }, 
        "4test-linacc-eul-100_Metawear_2020-02-11T13.05.36.569_C5013CAC38C1_Linear Acceleration_1.5.0.csv": {
            "session_name": "4test-linacc-eul-100",
            "session_metadata": "Metawear_2020-02-11T13.05.36.569_C5013CAC38C1",
            "session_key": "4test-linacc-eul-100_Metawear_2020-02-11T13.05.36.569_C5013CAC38C1",
            "sensor_mode": "linear acceleration",
            "firmware_version": "1.5.0",
        }, 
        "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1_Euler Angles_1.5.0.txt": {
            "session_name": "4test-linacc-eul-pr-100-0.99hz",
            "session_metadata": "Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "session_key": "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "sensor_mode": "euler angles",
            "firmware_version": "1.5.0",
        }, 
        "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1_Linear Acceleration_1.5.0.txt": {
            "session_name": "4test-linacc-eul-pr-100-0.99hz",
            "session_metadata": "Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "session_key": "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "sensor_mode": "linear acceleration",
            "firmware_version": "1.5.0",
        }, 
        "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1_Pressure_1.5.0.txt": {
            "session_name": "4test-linacc-eul-pr-100-0.99hz",
            "session_metadata": "Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "session_key": "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1",
            "sensor_mode": "pressure",
            "firmware_version": "1.5.0",
        }
    }

    for arg, ans in test_variables.items():
        for f in files: 
            if f.rsplit("\\", 1)[0] == arg:
                # Instantiate each MMRFile, then the MMRSession of the file
                mmr_file = mmrf.instantiate_mmr_file_from_path(f) 

                session = MMRSession(mmr_file)

                assert session.session_name == ans["session_name"]
                assert session.session_metadata == ans["session_metadata"]
                assert session.session_key == ans["session_key"]
                assert ans["sensor_mode"] in session.sensor_modes.keys()
                assert session.firmware_version == ans["firmware_version"]


def test_validate_sensor_modes():
    # Load files
    files = iof.load_csv_files()

    # TODO More entries might be required
    test_variables = {
        "4test-100-8g-500_Metawear_2020-02-11T13.28.11.448_C5013CAC38C1": {
            "sensor_modes": ["accelerometer", "gyroscope"]
        }, 
        "4test-linacc-eul-100_Metawear_2020-02-11T13.05.36.569_C5013CAC38C1": {
            "sensor_modes": ["euler angles", "linear acceleration"]
        }, 
        "4test-linacc-eul-pr-100-0.99hz_Metawear_2020-02-11T13.14.03.885_C5013CAC38C1": { 
            "sensor_modes": ["euler angles", "linear acceleration", "pressure"]
        }
    }

    # Instantiate all MMRSession objects
    sessions = [MMRSession(f) for f in mmrf.instantiate_mmr_files(files)]

    # Test
    for key, test in test_variables.items():
        for s in sessions:
            if key == s.session_key:
                assert s.sensor_modes == test["sensor_modes"]