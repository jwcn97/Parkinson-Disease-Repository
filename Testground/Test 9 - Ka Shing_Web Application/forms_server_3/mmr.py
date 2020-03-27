# === Imports ===
import re
from exceptions import UnsupportedNameFormatException
 
# === File ===
class File():
    """
    A class to handle each 'File' that's uploaded.

    Attributes
    ----------
    filename (str)
        The filename of the self.file variable. 
    file (FileStorage)
        Flask FileStorage object wrapping the file
    valid_extension (boolean)
        Whether the extension is valid
    """
    def __init__(self, file):
        """
        Constructor class.

        Parameters
        ----------
        file (FileStorage)
        """
        self.file = file
        self.filename = file.filename
        self.valid_extension = None


    def has_extension(self, extensions):
        """
        Checks that this file ends with any of the given extensions.

        Parameters
        ----------
        extensions (str[])
            An array of extensions to check again. 
        """
        self.valid_extension = False

        for e in extensions:
            if self.filename.endswith(e):
                self.valid_extension = True
                break 
            
# === MetaMotionR File === 
# File names regex
# Regex sections 
# 	1: Name, as given by whoever is using the Metawear app
#	2: Metadata, as given by the app
#	3: Type of data, e.g. Accelerometer, gyroscope
#	4: (Most likely) firmware version of the sensors
#	5: File extension
mmr_filename_regex = "(.*)_.*_(\d+-\d+-\d+T\d+\.\d+\.\d+\.\d+_\w+)_([\w\s]+)_(.*)\.(.*)"

class MMRFile(File):
    """
    A class to handle the data generated by MBientLab's MMR sensor.

    Attributes 
    ----------
    saved_name (str)
        The name saved by the user when taking the measurement. 
    metadata (str)
        The name appended by the sensor when taking the measurement. 
    sensor_mode (str)
        The mode of the sensor used for the measurement. 
    version (str)
        The version of the sensor.
    extension (str)
        The extension of the file.
    """
    def __init__(self, file):
        """
        Constructor class.

        Parameters
        ----------
        file (FileStorage) 
            Flask FileStorage wrapper.
        """
        super().__init__(file)


    def extract_metadata_from_filename(self):
        """
        Extracts metadata (if possible) from the filename

        Raises
        ------
        """
        extracted = re.search(mmr_filename_regex, self.filename)

        # Check if extracted is None
        if extracted is None: 
            raise UnsupportedNameFormatException("The filename does not match the given regex.")
        else:
            # Collect regex groups
            self.saved_name = extracted.group(1)
            self.metadata = extracted.group(2)
            self.sensor_mode = extracted.group(3)
            self.version = extracted.group(4)
            self.extension = extracted.group(5)

        
class MMRSession():
    """
    A class to handle each MetaMotionR session.

    Attributes
    ----------
    session_name (str)
        The name of the given session.
    mmr_files (dictionary, {})
        The dictionary of MMR files. The key is the sensor_mode, given in lowercase, of the MMRFile object it corresponds to. 
    valid_session (boolean)

    """
    def __init__(self, file):
        """
        Constructor class.

        Parameters
        ----------
        file (MMRFile())
        """
        self.session_name = '_'.join([file.saved_name, file.metadata])
        self.saved_name = file.saved_name
        self.metadata = file.metadata
        self.mmr_files = {}
        self.valid_session = None

        self.add_file(file)


    def add_file(self, file):
        """
        Adds the MMRFile object as one file run in this MMRSession. 

        Parameters
        ----------
        file (MMRFile)
        """
        self.mmr_files[file.sensor_mode.lower()] = file


    def validate_sensor_modes(self, modes):
        """
        Validates that this session has the desired modes.

        Parameters
        ----------
        modes (str[])
        """
        mode_check = list(map(lambda x: x.lower() in self.mmr_files.keys(), modes))
        self.valid_session = all(mode_check)
