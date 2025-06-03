"""
Python Extensions - Filesystem Tools Exception classes

---



"""

from enum import Enum

class FilesystemErrorCodesValues(Enum):
    """
    Filesystem Error Code enumerator
    """

    SUCCESS = 0
    PATH_IS_NOT_DIRECTORY = 1

class FilesystemErrorCodes:
    """
    Filesystem error code class

    ---

    This class provide error code and error code id (used by FilesystemErrorCodeValue enumerator)
    """
    __code: int
    __name: str

    def __init__(self, code: FilesystemErrorCodesValues):
        self.__code = code.value
        self.__name = code.name
        pass

    def code(self) -> int:
        return self.__code
    
    def name(self) -> str:
        return self.__name
    
    def ErrorCode(self) -> str:
        return f"{self.name()}({hex(self.code())})"

class FilesystemBaseException:
    """
    Filesystem Base Exception class to provide error code, error message
    and error details to all Filesystem exception classes.

    ---

    This class provide getters to all internal variables and an exception
    information exporter method
    """

    code: FilesystemErrorCodes
    message: str
    details: str

    def getCode(self) -> FilesystemErrorCodes:
        return self.code
    
    def getMessage(self) -> str:
        return self.message
    
    def getDetails(self) -> str:
        return self.details
    
    def getException(self) -> str:
        if len(self.details) > 0:
            return f"Code: {self.code.ErrorCode()} | Message: {self.message}\nDetails: {self.details}"
        else:
            return f"Code: {self.code.ErrorCode()} | Message: {self.message}"

class PathIsNotDirectory(Exception, FilesystemBaseException):
    """
    Path is not directory exception

    ---

    Exception used to throw a condition when a
    path should be a directory and a invalid path
    was used
    """

    def __init__ (self, message: str, details: str = ""):
        self.code = FilesystemErrorCodes(FilesystemErrorCodesValues.PATH_IS_NOT_DIRECTORY)
        self.message = message
        self.details = details
        pass