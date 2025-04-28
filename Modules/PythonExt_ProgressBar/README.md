# Python Progress Bar

Progress Bar is a Python 3 module to provide an easy way to print progress bars on console window output, using a minimum of two parameters: the total of items to be processed and the actual number of processed items. Both of the mandatory parameters should be a float type and four other optional parameters are: progress bar message (string type), show the percentage with decimal output (boolean type), alternative progress bar style (integer type) and the progress bar size (integer type).

## Using Python Progress Bar:

After import the progress bar module, set two float-point variables, the total of items and the actual value. Use them in the mandatory parameters positions of `progressBar` function. To use a progress bar properly, you must keep calling the function to provide the updated output, like using a loop statement. The function will reuse the last line or lines if you set a message on the console output and update the entire line to make sure no old information is keep.

This implementation has some limitations, like if you decide to not jump a line after the use of progress bar, part of the actual console line will contain the progress bar and the new line content. Similar behavior happens with progress bar when using a message output. The message uses the last line reuse the last line to write the content and can remove some important information in on console output. To avoid these situations, jump a new line.

### Progress Bar Messages:

The function allows you to send a message of the actual processing stage. The progress bar message uses the last console line to print the message and if the message does not fit in one line, it will cut the message resulting in the pattern: "exampl..."

To avoid this situation, make sure you are sending short messages that can fit in one line in you console.

If you leave the message empty which if the default value, no message will be generated. But, if you used before and for some reason send an empty message, the last line will not be updated.

### Progress Bar Decimal Percentage:

The original `progressBar` implementation does not used the percentage with decimal values avoiding the excessive use of characters. It's possible to use in this version, setting to `True` the `showDecimal` parameter. The default behavior still the original implementation.

Using the decimal percentage, will only use ONE decimal, and the internal algorithm will work to make sure all content of the progress bar can fit correctly in the console line, independent of the progress bar size used.

> **LIMITATION:** When using a integer value to register the actual components processed and set to `True` the `showDecimal` parameter, the percentage will return the decimal as **x.0%**

### About Alternate characters:

The `progressBar` function allows you to use two progress bar designs. The default use traditional characters 

Default character set (Set 0 to `useAlternateBarChars`):

[######.........] x%

When `useAlternateBarChars` set to **1** will make the progress bar like this:

[██████.........] x%

When `useAlternateBarChars` set to **2** will make the progress bar like this:

[■■■■■■_________] x%

**Any negative values or that not matches the acceptable ones, will return an exception of *Parameter out of range: useAlternateBarChars => value_used***

### Progress Bar Size:

The progress bar can be set to use four types of predefined size:
| Option | Size |
| ------ | ---- |
| 0 or default value | 50% of console width |
| 1 | 25% of console width |
| 2 | 75% of console width |
| 3 | 100% of console width |

If set any other value, the function `progressBar` will raise an IndexError exception with the message: *Parameter out of range: progressBarMaxLength => value_used*

## Example of basic progress bar usage:

```Python
import time
import PythonExt_ProgressBar

i = 0
iMax = 100
while i <= 100:
    PythonExt_ProgressBar.progressBar(iMax, i, f"Progressing {i}...", True, 0, 2)
    i += 1
    time.sleep(0.5)
    pass
print("")
```

# License

MIT License

Copyright (c) 2025 Matheus Lopes Silvati

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.