# Custom exceptions

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