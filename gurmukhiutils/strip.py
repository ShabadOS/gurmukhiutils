def strip(input, *removals):
    """
    Arg(s):
        input (string): The input string to modify.
        *removals: Variable length string arguments or
            a single tuple of string(s) to strip from input.

    Returns:
        string: The input without the specified removals.

    Example(s):
        >>> from gurmukhiutils.strip import strip
        >>> print(strip("ਸਬਦ. ਸਬਦ, ਸਬਦ; ਸਬਦ", ".", ","))
        ਸਬਦ ਸਬਦ ਸਬਦ; ਸਬਦ

        >>> from gurmukhiutils.strip import strip
        >>> VISHRAMS = [".", ",", ";"]
        >>> print(strip("ਸਬਦ. ਸਬਦ, ਸਬਦ; ਸਬਦ", VISHRAMS))
        ਸਬਦ ਸਬਦ ਸਬਦ ਸਬਦ

    """

    try:
        removals[0].split()
    except AttributeError:
        removals = removals[0]
    for removal in removals:
        input = input.replace(removal, "")

    return input


def strip_past(input, *removals):
    """
    Arg(s):
        input (string): The input string to modify.
        *removals: Variable length string arguments or
            a single tuple of string(s) to remove past.

    Returns:
        string: The input up to the first occurence of the
            specified removals.

    Example(s):
        >>> from gurmukhiutils.strip import strip_past
        >>> print(strip_past("ਸਬਦ. ਸਬਦ, ਸਬਦ; ਸਬਦ", ".", ","))
        ਸਬਦ

    """

    try:
        removals[0].split()
    except AttributeError:
        removals = removals[0]
    for removal in removals:
        if (index := input.find(removal)) >= 0:
            input = input[0:index]

    return input.rstrip()


def strip_line_endings(input):
    from gurmukhiutils.constants import LINE_ENDING_CHARS, LINE_ENDING_PATTERNS

    """
    Arg(s):
        input (string): The input string to modify.

    Returns:
        string: The input without line endings / end blocks.

    Example(s):
        >>> from gurmukhiutils.strip import strip_line_endings
        >>> print(strip_line_endings("ਸਬਦ ॥ ਸਬਦ ॥੧॥ ਰਹਾਉ ॥")
        ਸਬਦ ਸਬਦ

    """

    input = strip_past(input, LINE_ENDING_PATTERNS)

    for char in LINE_ENDING_CHARS:
        input = input.replace(char, "")

    while "  " in input:
        input = input.replace("  ", " ")

    return input.strip()
