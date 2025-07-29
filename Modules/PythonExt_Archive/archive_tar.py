"""
"""

import os
import sys
import tarfile

from .archive_general_tools import *
from .archive_logger import *

# Create an tar file to make the backup:
def mkTarFile(basepath: str, backup_fileName: str, compress: bool, backupDateTime: str = "", includeDateTime: bool = True) -> (tarfile.TarFile | int):
    """
    Make a TAR file
    ===================================

    Create a TAR file and return the object to reuse it.

    If an exception occur, the function will return 1

    Parameters
    -----------------------------------

    **basepath**: Path where the tar file will be stored

    **backup_fileName**: Base tar file name. The proper extension will be added depending on compress parameter.

    **compress**: If true, it will create a .tar.gzip file.

    **backupDateTime**: String with date and time information about the backup.

    Notes
    -----------------------------------

    1. If backupDateTime is empty, it will assume the backup is based on current date

    1.1. backupDateTime can be used as a reference to create a compression of older backups that was not archived

    """

    backup_dateTime = backupDateTime
    if backup_dateTime == "":
        backup_dateTime = getArchTimeStr(True, False, True)
        pass

    backup_extension = ".tar"

    if compress:
        backup_extension = ".tar.gz"
        pass

    backup_fullname = backup_fileName

    if includeDateTime:
        backup_fullname = f"{backup_fullname}_{backup_dateTime}"
        pass
    
    backup_fullname = backup_fullname + backup_extension
    backup_path = f"{basepath}/{backup_fullname}"

    try:
        if compress:
            tar = tarfile.open(backup_path, "x:gz", None, tarfile.GNU_FORMAT)
            pass
        else:
            tar = tarfile.open(backup_path, "x", None, tarfile.GNU_FORMAT)
            pass
        return tar
    except:
        print(f"Fail to create the tar file: {sys.exception()}")
        return 1

def add2TarFile(tarObj: tarfile.TarFile, workPath: str, path2Add: str, includeWorkPath: bool) -> int:
    """
    Add item to tar file
    ===================================

    Add a new path into the backup file
    
    This method return 0 if a file was add and 1 when it is a directory.
    
    In case of exception, will return -1. If the path does not exists, will return -2
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

# Make a TAR Backup
def makeTarBackup(backupListPaths: list[str], workingDirPath: str, backupBasePath: str, backupBaseFileName: str, baseBackupLogPath: str, compressBackupFile: bool, includeLogInBackupFile: int) -> int:
    """
    Make a TAR Backup
    ===================================

    Make a backup of the path list using the TAR format.

    It's possible to apply the compression on tar file, using the .tar.gzip format.

    Parameters
    -----------------------------------

    **backupListPaths**: List of paths to make the backup

    **workingDirPath**: Base working directory for the backup

    **backupBasePath**: Base location for the backup file

    **backupFileName**: Name for the TAR file that will receive the backup date and time in it's name

    **baseBackupLogPath**: Path to save the backup log. The log file will include the base backup file name and the backup date and time in it's name

    **compressBackupFile**: If True, will compress the file with .tar.gz extension

    **includeLogInBackupFile**: Determinate if the log file will be included inside the base of the backup file.

        Values available:

        0: (Default behavior) Do not include the log into the backup file

        1: Include the log into backup file and remove from original location

        2: Keep the log into the original location and inside the backup file
    
    Notes
    -----------------------------------

    1. If *includeLogInBackupFile* if not an acceptable value, the default behavior will be used
    """

    if not os.path.exists(workingDirPath):
        raise Exception("Can't find the working directory")
        pass
    
    if not os.path.exists(baseBackupLogPath):
        raise Exception("Can't find base location to log file")
        pass

    # Check includeLogInBackupFile default behavior if does not receive a compatible value:
    if includeLogInBackupFile < 0 or includeLogInBackupFile > 2:
        includeLogInBackupFile = 0
        pass

    backup_date_time = getArchTimeStr(True, False, True)
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

    tarObj = mkTarFile(tarFileBasePath, tarFileName, compressBackupFile, backup_date_time, True)

    # Add the base information about the backup file into the log:
    wrtArchLogEntry("Tar backup file", [tarCompletePath], backupLog)
    wrtArchLogEntry("Backup created", [getArchTimeStr(True, True, False)], backupLog)
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

    completeTime = getArchTimeStr(True, True, False)

    wrtArchLogEntry(f"Backup completed in time: {completeTime}", [], backupLog)
    backupLog.close()

    # Add the log file:
    if includeLogInBackupFile != 0:
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

    if includeLogInBackupFile == 1:
        if os.path.exists(backupLogPath):
            os.remove(backupLogPath)
            pass
        pass

    # Return zero if no error in the function was found:
    return 0