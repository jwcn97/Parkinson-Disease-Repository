# === Unsupported Name Format Exception ===
class UnsupportedNameFormatException(Exception):
    """
    An exception to be thrown when the MMR sensor's filename is unsupported by the given regex.
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None


    def __str__(self):
        if self.message:
            return 'UnsupportedNameFormatException, {0} '.format(self.message)
        else:
            return 'UnsupportedNameFormatException has been raised.'


# === Parameter Mismatch Exception ===
class ParameterMismatchException(Exception):
    """An exception raised when the number of parameter inputs don't match the number of parameters desired. 
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None


    def __str__(self):
        if self.message:
            return 'ParameterMismatchException, {0} '.format(self.message)
        else:
            return 'ParameterMismatchException has been raised.'