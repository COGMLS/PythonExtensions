"""
"""

from ..PythonExt_FilesystemTools import filesystem_exceptions

from enum import IntEnum

class PathNode:
    def __init__(self, data: str):
        self.data = data
        self.next = None
        pass
    pass

class PathType(IntEnum):
    UNKNOWN = -1        # Path exist, but it's type could not be determined
    NONE = 0            # Indicates that path has not been evaluated or an error occurred
    NOT_FOUND = 1       # Special treatment flag. Python 3.3 (Always defined if the path can not be founded)
    REGULAR_FILE = 2    # Common file (Python 3.6 >=)
    DIRECTORY = 3       # Directory (Python 3.6 >=)
    SYMLINK = 4         # Symbolic link (Python 3.6 >=)
    BLOCK = 5           # Block special file
    CHARACTER = 6       # Character special file
    FIFO = 7            # FIFO (also known as pipe) file
    SOCKET = 8          # Socket file
    JUNCTION = 9        # Junction path (Python 3.12 >=)
    HARDLINK = 10       # Hard link (Python 3.6 >=)
    MOUNT_POINT = 11    # Mount point (Python 3.4 >=)
    DEV_DRIVE = 12      # Windows only (Python 3.12 >=) | All platforms (Python 3.13)
    RESERVED = 13       # Windows only (Python 3.13 >=)
    pass