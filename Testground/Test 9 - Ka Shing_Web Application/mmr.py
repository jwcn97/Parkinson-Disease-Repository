# MMRFile() and MMRSession() classes representing a MetaMotionR (MMR) measurements file and session respectively.

# === Imports ===
import re
from exceptions import UnsupportedNameFormatException

# === MetaMotionR File ===
class MMRFile():
    """
    A class to hold each MetaMotionR sensor file.

    Attributes
    ----------
    filename(str)
        The name of the file
    session_name (str)
        The name of the session as given by the user when setting up the MetaBase app.
    session_metadata (str)
        The session metadata as generated by the MMR sennsor.
    session_key (str)
        #session_name# + "_" + #session_metadata#
    sensor_mode (str)
        The mode of the sensor associated with the file. This will be in lowercase.
    firmware_version (str)
        The version of the sensor firmware when the measurements were made.
    extension (str)
        The extension of the file.
    contents (str)
        The string within the FileStorage object.
    """
    def __init__(self, fs):
        """
        Instantiates the object's attributes with the given #fs# FileStorage object.

        Parameters
        ----------
        fs (FileStorage)
        """
        filename = fs.filename

        self.filename = filename

        # Get regex and match
        regex = "(.*)_.*_(\d+-\d+-\d+T\d+\.\d+\.\d+\.\d+_\w+)_([\w\s]+)_(.*)\.(.*)"

        match = re.search(regex, filename)

        # Check if match is None
        if match is None: 
            raise UnsupportedNameFormatException("The filename does not match the given regex.")
        else:
            # Collect regex groups
            self.session_name = match.group(1)
            self.session_metadata = match.group(2)
            self.session_key = '_'.join([self.session_name, self.session_metadata])
            self.sensor_mode = match.group(3).lower()
            self.firmware_version = match.group(4)
            self.extension = match.group(5)
            self.contents = fs.read().decode('utf-8')


# === MetaMotionR Session ===
class MMRSession():
    """A class to group MMRFile objects measured in the same session.

    Attributes:
    -----------
    session_name (str)
        The name of the session as given by the user when setting up the MetaBase app.
    session_metadata (str)
        The session metadata as generated by the MMR sennsor.
    session_key (str)
        #session_name# + "_" + #session_metadata#
    firmware_version (str)
        The version of the sensor firmware when the measurements were made.
    sensor_modes ({})
        The sensor-modes. 
        Key: The sensor mode of the desired MMR file, e.g. "accelerometer".
        Value: The MMRFile object.
    valid_session (boolean)
        Indicates whether the current session is valid based on the required sensor modes.
    """
    def __init__(self, mmrfile):
        """Extracts the following parameters from the given MMRFile:
         - session_name
         - session_metadata
         - session_key
         - firmware_version

        Then, adds the MMRFile object to a dictionary using the add_mmr_file() function. 

        Parameters
        ----------
        mmrfile (MMRFile)
        """
        self.session_name = mmrfile.session_name
        self.session_metadata = mmrfile.session_metadata
        self.session_key = mmrfile.session_key
        self.firmware_version = mmrfile.firmware_version
        self.sensor_modes = {}

        self.add_mmr_file(mmrfile) 

    
    def add_mmr_file(self, mmrfile):
        """Adds an MMRFile object to the session as a key-value pair in a dictionary.
        
        The key is the MMRFile's sensor_mode. The value is the MMRFile object. 

        Parameters
        ----------
        mmrfile (MMRFile)
        """
        self.sensor_modes[mmrfile.sensor_mode] = mmrfile


    def validate_sensor_modes(self, modes):
        """Checks that the current session contains all the required sensor modes.

        Parameters
        ----------
        modes (str[])
        """
        mode_check = list(map(lambda x: x.lower() in self.sensor_modes.keys(), modes))
        self.valid_session = all(mode_check)