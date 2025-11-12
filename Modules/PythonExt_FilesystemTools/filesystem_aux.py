"""
"""

import platform as _platform
import sys as _sys
import os.path as _os_path

from .filesystem_exceptions import *
from .filesystem_types import *

def fs_aux_hasAnyPattern() -> bool:
    return False

def fs_aux_count_PathNode(head: PathNode) -> int:
    if head is None:
        return 0
    i = 0

    curr = head
    i += 1

    while curr.next:
        curr = curr.next
        i += 1
        pass
    return i + 1 # Follow the methodology to start index in zero and end with +1 size

def fs_aux_list_content(head: PathNode) -> list[str]:
    tmpList = []

    if head is None:
        return []
    
    curr = head

    while True:
        if curr is None:
            break
        tmpList.append(curr.data)
        curr = curr.next
        pass

    return tmpList

def fs_aux_insert_pathNode(head: PathNode, newNode: str) -> PathNode:
    if newNode.startswith('/'):
        newNode = newNode.removeprefix('/')
        pass
    if newNode.startswith('\\'):
        newNode = newNode.removeprefix('\\')
        pass

    node = PathNode(newNode)

    if head is None:
        return node
    
    curr = head

    while curr.next:
        curr = curr.next
        pass

    curr.next = node
    return head

def fs_aux_PathNode_parent(head: PathNode) -> str:
    temp = ""
    tempList = fs_aux_list_content(head)
    i = 0
    iMax = len(tempList) - 1

    while i < iMax:
        temp += "/"
        i += 1
        pass
    if temp != "/" and temp.startswith('/') and _sys.platform == 'win32':
        temp = temp.removeprefix('/')
        pass
    if temp.endswith('/'):
        temp = temp.removesuffix('/')
        pass
    return temp

def fs_aux_PathNode_parent_node(head: PathNode) -> PathNode:
    i = 0
    size = fs_aux_count_PathNode(head)
    if size == 0:
        return PathNode("")
    newList: PathNode = None
    curr = head

    while curr.next:
        newList = fs_aux_insert_pathNode(newList, curr.data)
        i += 1
        if i < size - 1:
            break
        pass
    return newList

def fs_aux_remove_pathNode(head: PathNode, node: PathNode, index: int, data: str) -> PathNode:
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

def fs_aux_convert_pathNode2Str(head: PathNode) -> str:
    temp = ""

    curr = head

    while curr is not None:
        temp = temp + '/' + curr.data
        curr = curr.next
        pass
    if temp != "/" and temp.startswith('/') and _sys.platform == 'win32':
        temp = temp.removeprefix('/')
        pass
    return temp

def fs_aux_test_path_type(path: str) -> PathType:
    try:
        if not _os_path.exists(path):
            return PathType.NOT_FOUND
        if _os_path.isfile(path):
            return PathType.REGULAR_FILE
        if _os_path.isdir(path):
            return PathType.DIRECTORY
        if _os_path.islink(path):
            return PathType.SYMLINK
        if _os_path.ismount(path):
            return PathType.MOUNT_POINT
        if _platform.python_version_tuple()[1] >= 12:
            if _os_path.isjunction(path):
                return PathType.JUNCTION
            if _sys.platform == 'win32':
                if _os_path.isdevdrive(path):
                    return PathType.DEV_DRIVE
                pass
            pass
        if _platform.python_version_tuple()[1] >= 13:
            if _sys.platform == 'win32':
                if _os_path.isreserved(path):
                    return PathType.RESERVED
                pass
            if _os_path.isdevdrive(path):
                return PathType.DEV_DRIVE
            pass
        return PathType.UNKNOWN
    except:
        return PathType.NONE
        pass

    pass