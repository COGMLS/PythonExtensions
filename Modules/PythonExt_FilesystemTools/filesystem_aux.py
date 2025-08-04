"""
"""

import platform
import sys

from ..PythonExt_FilesystemTools import filesystem_exceptions
from ..PythonExt_FilesystemTools import filesystem_types

import os.path

def fs_aux_hasAnyPattern() -> bool:
    return False

def fs_aux_list_content(head: filesystem_types.PathNode) -> list[str]:
    tmpList = []
    curr = head

    while curr is not None:
        tmpList.append(curr.data)
        curr = curr.next
        pass

    return tmpList

def fs_aux_insert_pathNode(head: filesystem_types.PathNode, newNode: str) -> filesystem_types.PathNode:
    if newNode.startswith('/'):
        newNode = newNode.removeprefix('/')
        pass
    if newNode.startswith('\\'):
        newNode = newNode.removeprefix('\\')
        pass

    node = filesystem_types.PathNode(newNode)
    curr = head

    while curr is not None:
        curr = curr.next
        pass

    curr.next = node

    return curr

def fs_aux_remove_pathNode(head: filesystem_types.PathNode, node: filesystem_types.PathNode, index: int, data: str) -> filesystem_types.PathNode:
    searchType = 0 # 1: Index. 2: Data node search.

    if index >= 0:
        searchType = 1
        pass
    else:
        searchType = 2
        pass

    i = 0
    curr = head

    while curr is not None:
        if searchType == 1 and i != index or searchType == 2 and curr.data != data:
            curr = curr.next
            pass
        pass
    return curr

def fs_aux_convert_pathNode2Str(head: filesystem_types.PathNode) -> str:
    temp = ""

    curr = head

    while curr is not None:
        temp = temp + '/' + curr.data
        curr = curr.next
        pass
    return temp

def fs_aux_test_path_type(path: str) -> filesystem_types.PathType:
    try:
        if not os.path.exists(path):
            return filesystem_types.PathType.NOT_FOUND
        if os.path.isfile(path):
            return filesystem_types.PathType.REGULAR_FILE
        if os.path.isdir(path):
            return filesystem_types.PathType.DIRECTORY
        if os.path.islink(path):
            return filesystem_types.PathType.SYMLINK
        if os.path.ismount(path):
            return filesystem_types.PathType.MOUNT_POINT
        if platform.python_version_tuple()[1] >= 12:
            if os.path.isjunction(path):
                return filesystem_types.PathType.JUNCTION
            if sys.platform == 'win32':
                if os.path.isdevdrive(path):
                    return filesystem_types.PathType.DEV_DRIVE
                pass
            pass
        if platform.python_version_tuple()[1] >= 13:
            if sys.platform == 'win32':
                if os.path.isreserved(path):
                    return filesystem_types.PathType.RESERVED
                pass
            if os.path.isdevdrive(path):
                return filesystem_types.PathType.DEV_DRIVE
            pass
        return filesystem_types.PathType.UNKNOWN
    except:
        return filesystem_types.PathType.NONE
        pass

    pass