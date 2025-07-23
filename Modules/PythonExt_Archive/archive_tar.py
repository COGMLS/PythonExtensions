import os
import sys
import tarfile
import time
import io
import math

# Get the Date Time information as a string, using ISO 8601 format
# NOTE: If exportTimeZone is true but not exportTime, the time will be exported
# NOTE: timeStrCompatibleWithFs: Export the time string compatible with filesystems, using dash instead of two dots
def getTimeStr(exportTime: bool, exportTimeZone: bool, timeStrCompatibleWithFs: bool) -> str:
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

# Write the entries in the log object:
def wrtArchLogEntry(title: str, msg: str | list[str], logFile: io.TextIOWrapper) -> None:
    """
    Write Archive Log Entries
    ===================================

    White log entries for Archive module compatible functions

    Parameters
    -----------------------------------

    title: Set the title for log entry

    msg: Set the log message line(s). If is a multiple line message, the function will format the entries automatically

    logFile: A writable object file. This file must be opened to work.

    Notes
    -----------------------------------

    1) This function does not open or close the object file

    2) This function only writes the line endings with '\\n'

    3) When using multiple lines in msg parameter, the messages with receive a tabulation, indicating that are related to the title

    Example:

    [Title] :
        Message 1
        Message 2
        ...
    
    4) Using a single line message, the formatted entry will be: [Title]::Message

    5) If no message is set, the formatted entry will be: Title
    """

    if logFile.writable() and not logFile.closed :
        logFile.seek(0, io.SEEK_END)

        logEntry = ""

        if type(msg) == str:
            logEntry = f"{title}::{msg}\n"
            pass
        else:
            if len(msg) <= 1:
                if len(msg) == 1:
                    logEntry = f"{title}::{msg[0]}\n"
                    pass
                else:
                    logEntry = f"{title}\n"
                    pass
                pass
            else:
                logEntry = f"{title}:\n"
                for i in msg:
                    logEntry = logEntry + f"\t{i}\n"
                    pass
                pass
            pass

        if logEntry != "":
            logFile.writelines(logEntry)
            pass
    pass

# Get the complete path list, with more options to filter the files, directories and path patterns:
def getPathList2(path: str, excludeDirs: list[str] = [], excludeFiles: list[str] = [], excludeLinks: list[str] = [], excludePattern: list[str] = [], bListDir: bool = True, bListFiles: bool = True, bListLinks: bool = False, linksBehavior: int = 0) -> list[str]:
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

    1: Treat links as files.
    
    2: Follow links. The exclusions lists do not work with them. Except to excludeLinks list
    
    **Any other value will have the same meaning as zero**

    Notes
    -----------------------------------
    """
    
    if not os.path.exists(path):
        return list[str]
    
    pathList = []

    listDir = os.listdir(path)

    for i in listDir:
        pathType = 0 # 0: Directory | 1: File | 2: Link | 3: Other

        if os.path.isdir(i):
            pathType = 0
            pass
        elif os.path.isfile(i):
            pathType = 1
            pass
        elif os.path.islink(i):
            pathType = 2
            pass
        else:
            pathType = 3
            pass

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
            if pathType == 2 and linksBehavior == 1 or linksBehavior == 2:
                for j in excludeLinks:
                    if i == j:
                        bIsExcludePath = True
                        break
                    pass
                pass

            # Temporary path:
            p = path + "/" + i

            if not bIsExcludePath:

                # Check real path if is a link:
                if pathType == 2 and linksBehavior == 2:
                    p = os.path.realpath(p)
                    pass

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

            if not bIsExcludePath:
                if pathType == 0 and bListDir:
                    pathList.append(p)
                    pass
                if pathType == 1 and bListFiles:
                    pathList.append(p)
                    pass
                if pathType == 2 and (linksBehavior == 1 or linksBehavior == 2):
                    pathList.append(p)
                    pass
                pass
            pass

    return pathList

# Get the complete path list, with more options to filter the files, directories and path patterns:
def getPathList1(path: str, excludeDirs: list[str] = [], excludeFiles: list[str] = [], excludePattern: list[str] = [], bListDir: bool = True, bListFiles: bool = True) -> list[str]:
    """
    Get Path List (Old version)
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

# Create an tar file to make the backup:
def mkTarFile(basepath: str, backup_fileName: str, compress: bool, backupDateTime: str = "") -> (tarfile.TarFile | int):
    """
    """
    
    backup_dateTime = backupDateTime
    if backup_dateTime == "":
        backup_dateTime = getTimeStr(True, False, True)
        pass
    backup_extension = ".tar"

    if compress:
        backup_extension = ".tar.gz"
        pass

    backup_fullname = f"{backup_fileName}_{backup_dateTime}{backup_extension}"
    backup_path = f"{basepath}/{backup_fullname}"

    try:
        tar = tarfile.open(backup_path, "x:gz", None, tarfile.GNU_FORMAT)
        return tar
    except:
        print(f"Fail to create the tar file: {sys.exception()}")
        return 1

# Add a new path into the backup file
# This method return 0 if a file was add and 1 when it is a directory. In case of exception, will return -1. If the path does not exists, will return -2
def add2TarFile(tarObj: tarfile.TarFile, workPath: str, path2Add: str, includeWorkPath: bool) -> int:
    """
    """
    
    current_working_dir = os.getcwd()
    originalPath2Add = path2Add
    try:
        if os.path.exists(path2Add):
            if path2Add.startswith(workPath):
                path2Add = path2Add.removeprefix(workPath)
                if path2Add.startswith("/"):
                    if includeWorkPath:
                        wdn = os.path.basename(workPath)
                        path2Add = f"{wdn}{path2Add}"
                        pass
                    else:
                        path2Add = path2Add.removeprefix("/")
                        pass
                    pass
                pass
            pass
        else:
            return -2
        
        if includeWorkPath:
            #workDirName = os.path.basename(workPath)
            #workPath = workPath.removesuffix(f"/{workDirName}")
            workPath = os.path.dirname(workPath)
            pass

        os.chdir(workPath)
        tarObj.add(path2Add)
        os.chdir(current_working_dir)

        if os.path.isdir(originalPath2Add):
            return 1
        
        return 0
    except:
        os.chdir(current_working_dir) # Restore to original current working directory if fails
        print(f"Fail to add path: {path2Add} into tar file")
        print(f"Exception: {sys.exception()}")
        return -1

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

# Make a TAR Backup
# ---------Params------------
# backupListPaths: List of paths to make the backup
# workingDirPath: Base working directory for the backup
# backupBasePath: Base location for the backup file
# backupFileName: Name for the TAR file that will receive the backup date and time in it's name
# baseBackupLogPath: Path to save the backup log. The log file will include the base backup file name and the backup date and time in it's name
# compressBackupFile: If True, will compress the file with .tar.gz extension
# includeLogInBackupFile: If True will add the log file inside the base of the backup file and remove from the system temp folder
def makeTarBackup(backupListPaths: list[str], workingDirPath: str, backupBasePath: str, backupBaseFileName: str, baseBackupLogPath: str, compressBackupFile: bool, includeLogInBackupFile: bool) -> int:
    """
    """
    
    backup_date_time = getTimeStr(True, False, True)
    backupLogPath = f"{baseBackupLogPath}/{backupBaseFileName}_{backup_date_time}.log"

    backupLog = open(backupLogPath, 'wt', encoding="utf-8")
    backupLogBasePath = os.path.dirname(backupLogPath)

    # Prepare the TAR backup file:
    tarFileName = backupBaseFileName
    tarFileBasePath = backupBasePath
    tarCompletePath = f"{tarFileBasePath}/{tarFileName}"
    
    if os.path.exists(tarCompletePath):
        os.remove(tarCompletePath)
        pass

    tarObj = mkTarFile(tarFileBasePath, tarFileName, compressBackupFile, backup_date_time)

    # Add the base information about the backup file into the log:
    wrtArchLogEntry("Tar backup file", [tarCompletePath], backupLog)
    wrtArchLogEntry("Backup created", [getTimeStr(True, True, False)], backupLog)
    wrtArchLogEntry("---------------------------------------", [], backupLog)
    wrtArchLogEntry("Paths to backup", backupListPaths, backupLog)
    wrtArchLogEntry("---------------------------------------", [], backupLog)

    # Get the original working directory
    cwd = os.getcwd()

    # Prepare the backup counters:
    totalPaths = len(backupListPaths)
    actualPathsProcessed = 0

    backupOfDirs = 0
    backupOfFiles = 0
    backupFails = 0

    progressBar(totalPaths, actualPathsProcessed)

    backupArr = []

    # Backup the paths:
    for i in backupListPaths:
        b = i
        i = f"{os.path.basename(workingDirPath)}/{os.path.basename(b)}"
        status = add2TarFile(tarObj, workingDirPath, b, True)
        backupArr.append(f"{b} backup as TAR path: {i} | Status: {status}")
        if status == 0:
            backupOfFiles += 1
            pass
        elif status == 1:
            backupOfDirs += 1
            pass
        else:
            backupFails += 1
            pass
        actualPathsProcessed = actualPathsProcessed + 1
        progressBar(totalPaths, actualPathsProcessed)
        pass

    # Print the backup resume and close it:
    wrtArchLogEntry("Succeed backup paths", backupArr, backupLog)
    wrtArchLogEntry("---------------------------------------", [], backupLog)
    backupResume = [
        f"Total of paths to backup: {totalPaths}",
        f"Total of Directories: {backupOfDirs}",
        f"Total of Files: {backupOfFiles}",
        f"Total of Fails: {backupFails}"
    ]
    wrtArchLogEntry("Backup Resume", backupResume, backupLog)
    wrtArchLogEntry("---------------------------------------", [], backupLog)

    completeTime = getTimeStr(True, True, False)

    wrtArchLogEntry(f"Backup completed in time: {completeTime}", [], backupLog)
    backupLog.close()

    # Add the log file:
    if includeLogInBackupFile:
        os.chdir(backupLogBasePath)
        logName = backupLogPath.removeprefix(backupLogBasePath)
        if logName.startswith('/'):
            logName = logName.removeprefix('/')
            pass
        add2TarFile(tarObj, backupLogBasePath, logName, False)
        pass

    # Close the backup file:
    tarObj.close()

    # Restore the original working directory:
    os.chdir(cwd)

    # Remove the backup log is included into the backup file:
    backupLog.close()

    if includeLogInBackupFile:
        if os.path.exists(backupLogPath):
            os.remove(backupLogPath)
            pass
        pass

    # Return zero if no error in the function was found:
    return 0