"""
"""

from .filesystem_exceptions import *
from .filesystem_types import *
from .filesystem_aux import *

class Path:
    """
    Python Extension - Filesystem Tool - Path class

    This class provide the PathNode linked list storage and
    path type identification. It contains methods to convert
    the linked list to string path.
    """
    
    __head: PathNode
    __type: PathType

    def __init__(self, path: str, pathSeparatorTest = 2):
        PATH_SEPARATOR = ['/','\\']

        i = 0
        j = 0
        iMax = len(path)
        temp = ""

        while True:
            add2List = False

            if i < iMax:
                if path[i] == PATH_SEPARATOR[0] or path[i] == PATH_SEPARATOR[1]:
                    add2List = True
                    pass
                else:
                    temp += path[i]
                    pass
                pass
            else:
                add2List = True
                pass

            # Components and prevent empty names (except root) can be added:
            if add2List and temp != "" or add2List and temp == "" and j == 0:
                self.head = fs_aux_insert_pathNode(self.__head, temp)
                temp = ""
                j += 1
                pass

            if i == iMax:
                break
            i += 1
            pass
        pass

    def toString(self) -> str:
        return fs_aux_convert_pathNode2Str(self.__head)
    
    def type(self) -> PathType:
        return self.__type
    pass