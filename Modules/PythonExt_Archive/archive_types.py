"""
"""

import enum

class LinkPathAnalysisBehavior(enum.IntEnum):
    """
    Link path analysis behavior
    ---------------------------------------------

    Acceptable values to determinate the link path analysis in
    methods like getPathList2. Where links have special treatment
    and can be isolated from files and directories.
    """

    DO_NOT_ANALYZE = 0
    TREAT_AS_REGULAR_FILES = 1
    TREAT_AS_SPECIAL_FILES = 2
    FOLLOW_LINK_PATH = 3
    pass
