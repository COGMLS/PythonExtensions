"""
Python Extensions - Filesystem Python Extension Module

---


"""

import os
import os.path
import sys

import FilesystemExceptions

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

    if not os.path.isdir(path):
        raise FilesystemExceptions.PathIsNotDirectory("Path is not a directory")
        pass

    files = []

    if os.path.exists(path):
        if os.path.isdir(path):
            list = os.listdir(path)

            j = 0
            for i in list:
                list[j] = os.path.join(path, list[j])
                j = j + 1
                pass

            dirs = []

            for i in list:
                if os.path.isdir(i):
                    if (os.path.islink(i) and followLinks) or (not os.path.islink(i)):
                        dirs.append(i)
                        pass
                    if not includeDirectories:
                        list.remove(i)
                        pass
                    pass
                pass

            for i in list:
                if (os.path.isfile(i) and os.path.islink(i) and includeLinkFiles) or (os.path.isfile(i) and not os.path.islink(i)):
                    files.append(i)
                    pass
                if os.path.isdir(i) and includeDirectories:
                    if (os.path.islink(i) and includeLinkFiles) or (not os.path.islink(i)):
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

    if os.path.exists(path):
        if os.path.isdir(path):
            filesList += GetPathItems(path, False, False, False)
            pass
        else:
            filesList.append(path)
            pass
        pass

    return filesList

# Get the complete path list, with more options to filter the files, directories and path patterns:
def GetPathItems2 (path: str, excludeDirs: list[str] = [], excludeFiles: list[str] = [], excludePattern: list[str] = [], includeDirs: bool = True, includeFiles: bool = True, includeLinkFiles: bool = True, followLinks: bool = False) -> list[str]:
    if not os.path.exists(path):
        return list[str]
    
    pathList = []

    listDir = os.listdir(path)

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
            p = path + "/" + i
            if os.path.isdir(p):
                bAdd2List = True
                pass

            if os.path.isfile(p):
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
            if os.path.isfile(p) and includeFiles:
                pathList.append(p)
                pass
            if os.path.isdir(p) and includeDirs:
                pathList.append(p)
                pass
            pass

    return pathList