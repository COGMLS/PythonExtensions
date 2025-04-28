import os
import sys
import math

# Show a progress bar
def progressBar(totalItems: float, actualItemsProcessed: float, msgOutput: str = "", showDecimal: bool = False, useAlternateBarChars: int = 0, progressBarMaxLength: int = 0) -> None:
    """
    Progress Bar to console window, using an optional message output, with smart output formatter, optional decimal percentage output usage, optional bar size and alternative characters to draw the progress bar.

    NOTE: After the progress bar be processed by the last time, any new information into your console will replace the progress bar information and make probably messy to ready the new information. To avoid this, jump a new line after the progress bar usage.

    ---

    ABOUT THE MESSAGE OUTPUT:

    If no message is given or an empty message is send (""), no message output will be generated.

    Message output example (with parameter input: f"Processing {msg}"):
    
    Processing /path/file

    [######.........] x%
    
    NOTE: If the message is bigger than console window, the message will be modified, including "..." in the end.
    
    NOTE: When using a message, the line above will be reused. If you don't wan't to lose the console output information, jump a line before call for the first this method.

    ---

    ALTERNATIVE CHARACTERS:

    The parameter 'useAlternateBarChars' has three options: 0 (default), 1 and 2 values available.
    Any other values will raise the exception IndexError with the message: 'Parameter out of range: useAlternateBarChars => value_used'

    Using the default value (or setting to zero), will make the progress bar look like this:
    [######.........] x%

    When 'useAlternateBarChars' as '1' will make the progress bar look like this:
    [██████.........] x%

    When 'useAlternateBarChars' as '2' will make the progress bar look like this:
    [■■■■■■         ] x%

    ---

    PROGRESS BAR SIZE:

    The parameter 'progressBarMaxLength' has three options: 0 (default), 1 and 2 values available.
    Any other values will raise the exception IndexError with the message: 'Parameter out of range: progressBarMaxLength => value_used'

    On default value, the progress bar will use it's original size, using a maximum of 50% of the console width

    When the progressBarMaxLength is set to '1', it will use 25% of the console width

    When the progressBarMaxLength is set to '2', it will use 75% of the console width

    When the progressBarMaxLength is set to '3', it will use completely the console width

    NOTE: The progress bar adapts it's content to fit in the console window when using the 'showDecimal' is set to 'True'
    """
    
    consoleLength = os.get_terminal_size().columns

    completeBarChar = '#'
    emptyBarChar = '.'

    if useAlternateBarChars < 0 or useAlternateBarChars > 2:
        raise IndexError(f"Parameter out of range: useAlternateBarChars => {useAlternateBarChars}")
        pass

    if progressBarMaxLength < 0 or progressBarMaxLength > 3:
        raise IndexError(f"Parameter out of range: progressBarMaxLength => {progressBarMaxLength}")
        pass

    if useAlternateBarChars == 1:
        completeBarChar = '█'
        emptyBarChar = '.'
        pass
    if useAlternateBarChars == 2:
        completeBarChar = '■'
        emptyBarChar = ' '
        pass

    if len(msgOutput) > 0:
        if len(msgOutput) >= consoleLength:
            if len(msgOutput) == consoleLength:
                consoleLengthOverflow = -5
                pass
            else:
                consoleLengthOverflow = consoleLength - (len(msgOutput) + 5)
                pass
            msgOutput = msgOutput[:consoleLengthOverflow]
            msgOutput += "..."
            pass
        else:
            consoleLengthLeft = consoleLength - len(msgOutput)
            i = 0
            while i < consoleLengthLeft:
                msgOutput += ' '
                i = i + 1
                pass
            pass
        print(f"\033[F{msgOutput}\n", end='\r', flush=True, file=sys.stdout)
        pass

    barStart = f"Status:["
    barEnd = f"] "

    p = actualItemsProcessed / totalItems * 100.0

    if not showDecimal:
        p = math.floor(p)
        pass
    
    if p < 10:
        if showDecimal:
            barEnd = f"{barEnd}  {p:.1f}%"
            pass
        else:
            barEnd = f"{barEnd}  {p}%"
            pass
        pass
    elif p >= 10 and p < 100:
        if showDecimal:
            barEnd = f"{barEnd} {p:.1f}%"
            pass
        else:
            barEnd = f"{barEnd} {p}%"
            pass
        pass
    else:
        if showDecimal:
            barEnd = f"{barEnd}{p:.1f}%"
            pass
        else:
            barEnd = f"{barEnd}{p}%"
            pass
        pass

    bar = ""
    pBarExclusionLength = consoleLength / 2

    if progressBarMaxLength == 1:
        pBarExclusionLength = consoleLength * 3 / 4
        pass
    elif progressBarMaxLength == 2:
        pBarExclusionLength = consoleLength / 3
        pass
    elif progressBarMaxLength == 3:
        pBarExclusionLength = 0
        pass

    consoleLengthRemain = consoleLength - (len(barStart) + len(barEnd)) - pBarExclusionLength
    barDrawing = consoleLengthRemain * p / 100

    i = 0
    while i < consoleLengthRemain:
        if i <= barDrawing:
            bar = bar + completeBarChar
            pass
        else:
            bar = bar + emptyBarChar
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