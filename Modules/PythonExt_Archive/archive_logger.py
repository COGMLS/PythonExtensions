"""
Python Extensions - Archive: Logger submodule
===========================================================

This submodule contains a logger submodule function, to minimize
the complexity to write a log entry into a text based file.
"""

import io

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