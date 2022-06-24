from gurmukhiutils.constants import VISHRAMS


def strip(string: str, removals: list) -> str:
    """
    Strips substrings from a string.

    Args:
        string: The string to modify.
        removals: Any substring to remove.

    Returns:
        The string without any substrings.

    Examples:
        >>> strip("ਸਬਦ. ਸਬਦ, ਸਬਦ; ਸਬਦ", [".", ","])
        'ਸਬਦ ਸਬਦ ਸਬਦ; ਸਬਦ'

        >>> strip("ਸਬਦ. ਸਬਦ, ਸਬਦ; ਸਬਦ", gurmukhiutils.constants.VISHRAMS)
        'ਸਬਦ ਸਬਦ ਸਬਦ ਸਬਦ'

    """
    try:
        removals[0].split()
    except AttributeError:
        removals = removals[0]
    for removal in removals:
        string = string.replace(removal, "")

    return string


def strip_regex(string, patterns):
    """
    Strips regex patterns from a string.

    Args:
        string: The string to modify.
        patterns: Any pattern to remove.

    Returns:
        The string without any matching patterns.

    Example:
        >>> strip_regex("ਸਬਦ. ਸਬਦ, ਸਬਦ; ਸਬਦ", [".+\\s"])
        'ਸਬਦ'

    """
    import re

    try:
        patterns[0].split()
    except AttributeError:
        patterns = patterns[0]

    for pattern in patterns:
        string = re.sub(pattern, "", string)

    while "  " in string:
        string = string.replace("  ", " ")

    return string.strip()


def strip_line_endings(input: str) -> str:
    """
    Removes line endings.

    Arg:
        input: The input string to modify.

    Returns:
        The input without line endings.

    Example:
        >>> strip_line_endings("ਸਬਦ ॥ ਸਬਦ ॥੧॥ ਰਹਾਉ ॥")
        'ਸਬਦ ਸਬਦ'

    """
    line_ending_patterns = [
        "[।॥] ਰਹਾਉ.*",
        "[।॥][੦-੯].*",
        "\\|\\|\\d.*",
        "\\|\\|Pause.*",
        "[।॥(\\|\\|)]",
    ]

    return strip_regex(input, line_ending_patterns)


def strip_vishrams(input: str) -> str:
    """
    Removes all vishram characters.

    Arg:
        input: The input string to modify.

    Returns:
        The input without vishrams.

    Example:
        >>> strip_vishrams(ਸਬਦ. ਸਬਦ, ਸਬਦ; ਸਬਦ ॥)
        'ਸਬਦ ਸਬਦ ਸਬਦ ਸਬਦ ॥'

    """
    from gurmukhiutils.constants import VISHRAMS

    return strip(input, VISHRAMS)
