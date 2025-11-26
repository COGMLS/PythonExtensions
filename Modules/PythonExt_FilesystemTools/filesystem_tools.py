"""
Python Extensions - Filesystem Tools for Python Extension

---



"""

import os as _os
import os.path as _os_path
import sys as _sys

from .filesystem_exceptions import *

# Method to remove items from given path, including directories recursively and non-empty directories.
def remove_item_path(path: str) -> None:
    """
    ABOUT THIS METHOD:
    
    Remove a given item from path
    
    Method to remove items from given path, including directories
    recursively and non-empty directories. Only mount point paths
    can not be send to this function. Any junction or symbolic
    link are treated as a *regular file* and is removed. **There are
    no interactions with links.**

    PARAMETER INFORMATION:

    path: Path to directory/file/link/junction

    RETURN VALUES:

    This method does not return any value

    EXCEPTIONS:

    If the given path is not a existing path, it will raise an exception.

    If the given path is a mount point, it will raise an exception.
    """
    if not _os_path.exists(path):
        raise Exception(f"Path {path} does not exist!")
    
    if _os_path.isfile(path) or _os_path.isjunction(path) or _os_path.islink(path):
        _os.remove(path)
        pass

    if _os_path.isdir(path) and not _os_path.ismount(path):
        dir_content = _os.listdir(path)
        
        if len(dir_content) == 0:
            _os.rmdir(path)
            pass
        else:
            for i in dir_content:
                if not _sys.platform.startswith("win32"):
                    i = _os_path.join(path, i)
                    pass
                remove_item_path(i)
                pass
            _os.rmdir(path)
            pass
        pass

    if _os_path.ismount(path):
        raise Exception(f"The path {path} is a mount point!")
    pass