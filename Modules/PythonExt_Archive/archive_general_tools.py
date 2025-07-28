"""
"""

import os
import sys
import time
import math

from .archive_types import LinkPathAnalysisBehavior

# Get the Date Time information as a string, using ISO 8601 format
# NOTE: If exportTimeZone is true but not exportTime, the time will be exported
# NOTE: timeStrCompatibleWithFs: Export the time string compatible with filesystems, using dash instead of two dots
def getArchTimeStr(exportTime: bool, exportTimeZone: bool, timeStrCompatibleWithFs: bool) -> str:
    """
    Get Time String
    =========================

    Get the date and time string in ISO 8601 format

    Parameters
    -------------------------

    exportTime: Export the time. If false, it will export only date

    exportTimeZone: Export the time zone information

    timeStrCompatibleWithFs: Make the string output compatible with filesystems avoiding specific characters '/' and ':'

    Notes
    -------------------------

    1) If exportTimeZone is true but not exportTime, the time will be exported

    2) timeStrCompatibleWithFs: Export the time string compatible with filesystems, using dash instead of two dots
    """

    timeStr = ""

    if not exportTime and exportTimeZone:
        exportTime = True
        pass

    lTime = time.localtime()
    # Time String for Year-Month-Day:
    month = f"{lTime.tm_mon}"
    day = f"{lTime.tm_mday}"

    if lTime.tm_mon < 10:
        month = f"0{month}"
        pass
    if lTime.tm_mday < 10:
        day = f"0{day}"
        pass

    if timeStrCompatibleWithFs:
        timeStr = f"{lTime.tm_year}-{month}-{day}"
        pass
    else:
        timeStr = f"{lTime.tm_year}/{month}/{day}"
        pass

    # Complete Date Time info for YYYY-MM-dd_HH-mm-ssT<TimeZone>:
    hour = f"{lTime.tm_hour}"
    minute = f"{lTime.tm_min}"
    second = f"{lTime.tm_sec}"

    if lTime.tm_hour < 10:
        hour = f"0{lTime.tm_hour}"
        pass
    if lTime.tm_min < 10:
        minute = f"0{lTime.tm_min}"
        pass
    if lTime.tm_sec < 10:
        second = f"0{lTime.tm_sec}"
        pass

    if exportTime:
        if timeStrCompatibleWithFs:
            timeStr = f"{timeStr}_{hour}-{minute}-{second}"
            pass
        else:
            timeStr = f"{timeStr} {hour}:{minute}:{second}"
            pass
        pass

    if exportTimeZone:
        timeStr = f"{timeStr}T{lTime.tm_zone}"
        #if timeStrCompatibleWithFs:
        #    pass
        #else:
        #    timeStr = f"{timeStr} T {lTime.tm_zone}"
        #    pass
        pass

    return timeStr

# Get the complete path list, with more options to filter the files, directories and path patterns:
def getPaths2Arch(path: str, excludeDirs: list[str] = [], excludeFiles: list[str] = [], excludePattern: list[str] = [], bListDir: bool = True, bListFiles: bool = True) -> list[str]:
    """
    Get Paths List to Archive (Old version)
    ===================================

    Function to get files and directories with support to filter files, directories and path patterns.

    Parameters
    -----------------------------------

    **path**: Path to get verified.

    **excludeDirs**: list of directory names to exclude from analysis

    **excludeFiles**: list of files that will be excluded from analysis

    **excludePattern**: list of patterns in a path (file or directory) to exclude

    **bListDir**: Include directories into path analysis

    **bListFiles**: Include files into path analysis

    Notes
    -----------------------------------
    """
    
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
            if os.path.isfile(p) and bListFiles:
                pathList.append(p)
                pass
            if os.path.isdir(p) and bListDir:
                pathList.append(p)
                pass
            pass

    return pathList

# Get the complete path list, with more options to filter the files, directories and path patterns:
def getPaths2Arch2(path: str, excludeDirs: list[str] = [], excludeFiles: list[str] = [], excludeLinks: list[str] = [], excludePattern: list[str] = [], bListDir: bool = True, bListFiles: bool = True, bListLinks: bool = False, linksBehavior: int = 0) -> list[str]:
    """
    Get Path List 2
    ===================================

    Function to get files and directories with support to filter files, directories and path patterns.

    This method has optimizations to work in very large analysis scenarios, with reduced loop checking and tests for links

    Parameters
    -----------------------------------

    **path**: Path to get verified.

    **excludeDirs**: list of directory names to exclude from analysis

    **excludeFiles**: list of files that will be excluded from analysis

    **excludeLinks**: list of links names that will be excluded from analysis

    **excludePattern**: list of patterns in a path (file or directory) to exclude

    **bListDir**: Include directories into path analysis

    **bListFiles**: Include files into path analysis

    **bListLinks**: Include link files into path analysis

    **linksBehavior**: A numerical value that determinate how to treat links during analysis

    Values available:

    0: Do not analyze links. (Skip then)

    1: Treat links as regular files.
    
    2: Treat links as particular files (They only will be added when bListLinks is True)
    
    3: Follow links. The exclusions lists do not work with them. Except to excludeLinks and excludePattern lists
    
    **Any other value will have the same meaning as zero**

    Notes
    -----------------------------------

    1. Links behavior are affected by bListFiles and bListDirs (when behavior is set to 1).

    1.1. If links are treated as regular files, bListFiles should be true to add them into the list

    1.2. If links should be followed, the real path will only be added depending of type of destination path and if bListFiles and/or bListDirs are true.
    """
    
    if not os.path.exists(path):
        return list[str]
    
    if linksBehavior < 0 or linksBehavior > 3:
        linksBehavior = LinkPathAnalysisBehavior.DO_NOT_ANALYZE
        pass
    
    pathList = []

    listDir = os.listdir(path)

    for i in listDir:
        pathType = -1 # 0: Directory | 1: File | 2: Link | 3: Other (-1 initialization value)
        linkDestType = -1 # Link destination path type. Same as pathType, but test the real path pointed by the link

        # Temporary path:
        p = path + "/" + i

        if os.path.isdir(p):
            pathType = 0
            pass
        elif os.path.isfile(p):
            pathType = 1
            pass
        elif os.path.islink(p):
            pathType = 2
            pass
        else:
            pathType = 3
            pass

        # Exclude the links if they are treated as special files and not listed in path list or if they should not be analyzed:
        if pathType == 2 and ((linksBehavior == LinkPathAnalysisBehavior.TREAT_AS_SPECIAL_FILES and not bListLinks) or linksBehavior == LinkPathAnalysisBehavior.DO_NOT_ANALYZE):
            pathType = 3 # Change to pathType to skip all other tests
            pass

        # If is file, directory or link, start the exclusion lists analysis:
        if pathType < 3:
            bIsExcludePath = False

            if pathType == 0:
                for j in excludeDirs:
                    if i == j:
                        bIsExcludePath = True
                        break
                    pass
                pass
            if pathType == 1:
                for j in excludeFiles:
                    if i == j:
                        bIsExcludePath = True
                        break
                    pass
                pass
            if pathType == 2:
                for j in excludeLinks:
                    if i == j:
                        bIsExcludePath = True
                        break
                    pass
                pass

            if not bIsExcludePath:

                # Check real path if should follow the link path:
                if pathType == 2 and linksBehavior == LinkPathAnalysisBehavior.FOLLOW_LINK_PATH:
                    p = os.path.realpath(p)

                    # Test link real path and classify:
                    if os.path.isdir(p):
                        linkDestType = 0
                        pass
                    elif os.path.isfile(p):
                        linkDestType = 1
                        pass
                    else:
                        linkDestType = 3 # Other (skip analysis)
                        bIsExcludePath = True # Exclude path analysis
                        pass
                    pass
                pass

            if not bIsExcludePath:
                # Exclude items that matches on path patterns exclusion list:
                for j in excludePattern:
                    if j.startswith('*') and j.endswith('*'):
                        j = j.removeprefix('*')
                        j = j.removesuffix('*')
                        if p.__contains__(j):
                            bIsExcludePath = True
                            break
                        pass
                    if j.endswith('*') and not j.startswith('*'):
                        j = j.removesuffix('*')
                        if i.startswith(j):
                            bIsExcludePath = True
                            break
                        pass
                    if j.startswith('*') and not j.endswith('*'):
                        j = j.removeprefix('*')
                        if i.endswith(j):
                            bIsExcludePath = True
                            break
                        pass
                    pass
                pass

            # If the path was not excluded, test if it should be listed:
            if not bIsExcludePath:
                if pathType == 0 and bListDir:
                    pathList.append(p)
                    pass
                if pathType == 1 and bListFiles:
                    pathList.append(p)
                    pass
                if pathType == 2:
                    # If the links should be treat as files, only add then if files should be added:
                    if linksBehavior == LinkPathAnalysisBehavior.TREAT_AS_REGULAR_FILES and bListFiles:
                        pathList.append(p)
                        pass
                    # If the links should be treat as special files, only add then if bListLinks is enabled:
                    if linksBehavior == LinkPathAnalysisBehavior.TREAT_AS_SPECIAL_FILES and bListLinks:
                        pathList.append(p)
                        pass
                    # If the links should be followed, treat check type of path with the listing parameters set:
                    if linksBehavior == LinkPathAnalysisBehavior.FOLLOW_LINK_PATH:
                        if linkDestType == 0 and bListDir:
                            pathList.append(p)
                            pass
                        if linkDestType == 1 and bListFiles:
                            pathList.append(p)
                            pass
                        pass
                    pass
                pass
            pass

    return pathList

# Show a progress bar
def progressBar(totalPaths, actualPathsProcessed) -> None:
    consoleLength = os.get_terminal_size().columns
    barStart = f"Status:["
    barEnd = f"] "
    p = actualPathsProcessed / totalPaths * 100
    p = math.floor(p)
    
    if p < 10:
        barEnd = f"{barEnd}  {p}/100"
        pass
    elif p >= 10 and p < 100:
        barEnd = f"{barEnd} {p}/100"
        pass
    else:
        barEnd = f"{barEnd}{p}/100"
        pass

    bar = ""

    consoleLengthRemain = consoleLength - (len(barStart) + len(barEnd)) - 50
    barDrawing = consoleLengthRemain * p / 100

    i = 0
    while i < consoleLengthRemain:
        if i <= barDrawing:
            bar = bar + '█'
            pass
        else:
            bar = bar + '.'
            pass
        i = i + 1
        pass

    bar = barStart + bar + barEnd

    if p < 100:
        print(bar, end='\r', flush=True, file=sys.stdout)
        pass
    else:
        print(bar, end='\n', flush=True, file=sys.stdout)
        pass
    pass