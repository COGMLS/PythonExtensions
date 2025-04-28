"""
Python Progress Bar
===================

Progress Bar is a Python 3 module to provide an easy way to print
progress bars on console window output, using a minimum of two
parameters: the total of items to be processed and the actual number
of processed items. Both of the mandatory parameters should be a float
type and four other optional parameters are: progress bar message
(string type), show the percentage with decimal output (boolean type),
alternative progress bar style (integer type) and the progress bar
size (integer type).

Using Python Progress Bar:
--------------------------

After import the progress bar module, set two float-point variables,
the total of items and the actual value. Use them in the mandatory
parameters positions of `progressBar` function. To use a progress bar
properly, you must keep calling the function to provide the updated
output, like using a loop statement. The function will reuse the last
line or lines if you set a message on the console output and update
the entire line to make sure no old information is keep.

This implementation has some limitations, like if you decide to not
jump a line after the use of progress bar, part of the actual console
line will contain the progress bar and the new line content.
Similar behavior happens with progress bar when using a message output.
The message uses the last line reuse the last line to write the content
and can remove some important information in on console output.
To avoid these situations, jump a new line.
"""

from .progressBar import *