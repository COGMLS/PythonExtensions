"""
Python Extensions - Filesystem Python Extension Module

---


"""

import os as _os
import os.path as _os_path
import sys as _sys

from .filesystem_exceptions import *

# Get the files list:
def GetPathItems (path: str, followLinks: bool = False, includeDirectories: bool = True, includeLinkFiles: bool = False) -> list[str]:
    """
    ABOUT THIS METHOD:

    Get the list of items inside a directory

    ---

    PARAMETER INFORMATION:

    path: Directory path to get the files list

    followLinks: If True, it will follow the links available

    includeDirectories: If True, the files list will include the directories in the output list

    includeLinkFiles: If True, will include the link files into the output list

    RETURN VALUE:

    This method returns a list of strings representing the paths founded.

    If the list is empty, no file, directory and link, if included those last components was set
    """

    if not _os_path.isdir(path):
        raise PathIsNotDirectory("Path is not a directory")
        pass

    files = []

    if _os_path.exists(path):
        if _os_path.isdir(path):
            list = _os.listdir(path)

            if _sys.platform != 'win32':
                j = 0
                while j < len(list):
                    list[j] = _os_path.join(path, list[j])
                    j = j + 1
                    pass
                pass

            dirs = []

            for i in list:
                if _os_path.isdir(i):
                    if (_os_path.islink(i) and followLinks) or (not _os_path.islink(i)):
                        dirs.append(i)
                        pass
                    if not includeDirectories:
                        list.remove(i)
                        pass
                    pass
                pass

            for i in list:
                if (_os_path.isfile(i) and _os_path.islink(i) and includeLinkFiles) or (_os_path.isfile(i) and not _os_path.islink(i)):
                    files.append(i)
                    pass
                if _os_path.isdir(i) and includeDirectories:
                    if (_os_path.islink(i) and includeLinkFiles) or (not _os_path.islink(i)):
                        files.append(i)
                        pass
                    pass
                pass

            for i in dirs:
                files += GetPathItems(i, followLinks, includeDirectories, includeLinkFiles)
                pass
            pass
        else:
            files.append(path)
            pass
        pass

    return files

# Function to list files:
def ListFiles (path: str) -> list[str]:
    """
    This method call GetPathItems configured to only list files inside a directory
    """
    filesList = []

    if _os_path.exists(path):
        if _os_path.isdir(path):
            filesList += GetPathItems(path, False, False, False)
            pass
        else:
            filesList.append(path)
            pass
        pass

    return filesList

# Get the complete path list, with more options to filter the files, directories and path patterns:
def GetPathItems2 (path: str, excludeDirs: list[str] = [], excludeFiles: list[str] = [], excludePattern: list[str] = [], includeDirs: bool = True, includeFiles: bool = True, includeLinkFiles: bool = True, followLinks: bool = False) -> list[str]:
    if not _os_path.exists(path):
        return list[str]
    
    pathList = []

    listDir = _os.listdir(path)

    for i in listDir:
        bIsExcludeDir = False
        bIsExcludeFile = False

        for j in excludeDirs:
            if i == j:
                bIsExcludeDir = True
                break
            pass

        for j in excludeFiles:
            if i == j:
                bIsExcludeFile = True
                break
            pass

        bAdd2List = False

        if not bIsExcludeDir and not bIsExcludeFile:
            if _sys.platform != 'win32':
                p = _os_path.join(path, i)
                pass

            if _os_path.isdir(p):
                bAdd2List = True
                pass

            if _os_path.isfile(p):
                bAdd2List = True
                pass

            for j in excludePattern:
                if j.startswith('*') and j.endswith('*'):
                    j = j.removesuffix('*')
                    j = j.removeprefix('*')
                    if p.__contains__(j):
                        bAdd2List = False
                        break
                    pass
                
                if j.endswith('*') and not j.startswith('*'):
                    j = j.removesuffix('*')
                    if i.startswith(j):
                        bAdd2List = False
                        break
                    pass
                
                if j.startswith('*') and not j.endswith('*'):
                    j = j.removeprefix('*')
                    if i.endswith(j):
                        bAdd2List = False
                        break
                    pass
                pass

        if bAdd2List:
            if _os_path.isfile(p) and includeFiles:
                pathList.append(p)
                pass
            if _os_path.isdir(p) and includeDirs:
                pathList.append(p)
                pass
            pass

    return pathList