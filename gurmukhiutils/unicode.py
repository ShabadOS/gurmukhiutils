import re
from typing import Literal, Match

UNICODE_STANDARDS = Literal["Unicode Consortium", "Sant Lipi"]


def unicode(
    string: str,
    unicode_standard: Literal[UNICODE_STANDARDS] = "Unicode Consortium",
) -> str:
    """
    Converts any ascii gurmukhi characters and sanitizes to unicode gurmukhi.

    Note:
        Converting yayya (ਯ) variants with an open-top using the Unicode Consortium standard is considered destructive. This function will substitute the original with it's shirorekha/top-line equivalent.

        Many fonts and text shaping engines fail to render half-yayya (੍ਯ) correctly. Regardless of the standard used, it is recommended to use the Sant Lipi font mentioned below.

    Args:
        string: The string to affect.

        unicode_standard: The mapping system to use. The default is unicode compliant and can render 99% of the Shabad OS Database. The other option "Sant Lipi" is intended for a custom unicode font bearing the same name (see: https://github.com/shabados/SantLipi). Defaults to "Unicode Consortium".

    Returns:
        A string whose Gurmukhi is normalized to a Unicode standard.

    Examples:
        >>> unicode("123")
        '੧੨੩'

        >>> unicode("<> > <")
        'ੴ ☬ ੴ'

        >>> unicode("gurU")
        'ਗੁਰੂ'
    """

    # AnmolLipi/GurbaniAkhar & GurbaniLipi by Kulbir S. Thind, MD
    ASCII_TO_UNICODE_MAP = {
        "a": "ੳ",
        "b": "ਬ",
        "c": "ਚ",
        "d": "ਦ",
        "e": "ੲ",
        "f": "ਡ",
        "g": "ਗ",
        "h": "ਹ",
        "i": "ਿ",
        "j": "ਜ",
        "k": "ਕ",
        "l": "ਲ",
        "m": "ਮ",
        "n": "ਨ",
        "o": "ੋ",
        "p": "ਪ",
        "q": "ਤ",
        "r": "ਰ",
        "s": "ਸ",
        "t": "ਟ",
        "u": "ੁ",
        "v": "ਵ",
        "w": "ਾ",
        "x": "ਣ",
        "y": "ੇ",
        "z": "ਜ਼",
        "A": "ਅ",
        "B": "ਭ",
        "C": "ਛ",
        "D": "ਧ",
        "E": "ਓ",
        "F": "ਢ",
        "G": "ਘ",
        "H": "੍ਹ",
        "I": "ੀ",
        "J": "ਝ",
        "K": "ਖ",
        "L": "ਲ਼",
        "M": "ੰ",
        "N": "ਂ",
        "O": "ੌ",
        "P": "ਫ",
        "Q": "ਥ",
        "R": "੍ਰ",
        "S": "ਸ਼",
        "T": "ਠ",
        "U": "ੂ",
        "V": "ੜ",
        "W": "ਾਂ",
        "X": "ਯ",
        "Y": "ੈ",
        "Z": "ਗ਼",
        "0": "੦",
        "1": "੧",
        "2": "੨",
        "3": "੩",
        "4": "੪",
        "5": "੫",
        "6": "੬",
        "7": "੭",
        "8": "੮",
        "9": "੯",
        "[": "।",
        "]": "॥",
        "\\": "ਞ",
        "|": "ਙ",
        "`": "ੱ",
        "~": "ੱ",
        "@": "ੑ",
        "^": "ਖ਼",
        "&": "ਫ਼",
        "†": "੍ਟ",  # dagger symbol
        "ü": "ੁ",  # u-diaeresis letter
        "®": "੍ਰ",  # registered symbol
        "\u00b4": "ੵ",  # acute accent (´)
        "\u00a8": "ੂ",  # diaeresis accent (¨)
        "µ": "ੰ",  # mu letter
        "æ": "਼",
        "\u00a1": "ੴ",  # inverted exclamation (¡)
        "ƒ": "ਨੂੰ",  # florin symbol
        "œ": "੍ਤ",
        "Í": "੍ਵ",  # capital i-acute letter
        "Î": "੍ਯ",  # capital i-circumflex letter
        "Ï": "ੵ",  # capital i-diaeresis letter
        "Ò": "॥",  # capital o-grave letter
        "Ú": "ਃ",  # capital u-acute letter
        "\u02c6": "ਂ",  # circumflex accent (ˆ)
        "\u02dc": "੍ਨ",  # small tilde (˜)
        #
        #
        "<>": "ੴ",  # AnmolLipi/GurbaniAkhar variant
        "<": "ੴ",  # GurbaniLipi variant
        ">": "☬",  # GurbaniLipi variant
        #
        "Åå": "ੴ",  # AnmolLipi/GurbaniAkhar variant
        "Å": "ੴ",  # GurbaniLipi variant
        "å": "ੴ",  # GurbaniLipi variant
        #
        #
        # AnmolLipi/GurbaniAkhar mappings:
        "§": "੍ਹੂ",  # section symbol
        "¤": "ੱ",  # currency symbol
        #
        #
        # GurbaniLipi mappings:
        "ç": "੍ਚ",  # c-cedilla letter
        #
        #
        # AnmolLipi/GurbaniAkhar overriding GurbaniLipi mapping:
        "Ç": "☬",  # khanda instead of california state symbol
        #
        #
        # Miscellaneous:
        "\u201a": "❁",  # single low-9 quotation (‚) mark
        #
        #
        # Nullify
        "Æ": "",  # This is either the 2nd portion of ੴ or a symbol of USA. The ੴ renders correctly according to rules above.
        "Ø": "",  # This is a topline / shirorekha (शिरोरेखा) extender
        "ÿ": "",  # This is the author Kulbir S Thind's stamp
        "Œ": "",  # Box drawing left flower
        "‰": "",  # Box drawing right flower
        "Ó": "",  # Box drawing top flower
        "Ô": "",  # Box drawing bottom flower
    }

    # OpenGurbaniAkhar by Sarabveer Singh (GurbaniNow)
    SANT_LIPI_MAP = {
        "Î": "꠳ਯ",  # replace capital i-circumflex letter with indic one-sixteenth + yayya = half-yayya
        "੍ਯ": "꠳ਯ",  # replace unicode half-yayya with same as above
        "ï": "꠴ਯ",  # replace i-diaeresis letter with indic one-eight + yayya = open-top full yayya
        "î": "꠵ਯ",  # replace i-circumflex letter with indic three-sixtenths + yayya = open-top half-yayya
    }

    SANT_LIPI_TO_STANDARD_MAP = {
        "꠳ਯ": "੍ਯ",
        "꠴ਯ": "ਯ",
        "꠵ਯ": "੍ਯ",
    }

    # Move ASCII sihari before mapping to unicode
    ASCII_BASE_LETTERS = "a-zA-Z\\|^&Îîï"
    ASCII_SIHARI_PATTERN = rf"(i)([{ASCII_BASE_LETTERS}])"
    string = re.sub(ASCII_SIHARI_PATTERN, r"\2\1", string)

    # Replace any ASCII with Unicode Gurmukhi
    for key, value in ASCII_TO_UNICODE_MAP.items():
        string = string.replace(key, value)

    for key, value in SANT_LIPI_MAP.items():
        string = string.replace(key, value)

    # Normalize Unicode
    string = unicode_normalize(string)

    if unicode_standard == "Unicode Consortium":

        # Map Sant Lipi to Unicode Consortium
        for key, value in SANT_LIPI_TO_STANDARD_MAP.items():
            string = string.replace(key, value)

    return string


def unicode_normalize(string: str) -> str:
    """
    Normalizes Gurmukhi according to Unicode Standards.

    Arg:
        string: The string to affect.

    Returns:
        Returns a string containing normalized gurmukhi.

    Example:
        >>> unicode_normalize("Hello ਜੀ")
        'Hello ਜੀ'
    """

    string = sort_diacritics(string)

    string = sanitize_unicode(string)

    return string


def sort_diacritics(string: str) -> str:
    """
    Orders the gurmukhi diacritics in a string according to Unicode standards.

    Note:
        Not intended for base letters with multiple subjoined letters.

    Arg:
        string: The string to affect.

    Returns:
        The same string with gurmukhi diacritics arranged in a sorted manner.

    Example:
        >>> sort_diacritics("\u0a41\u0a4b") == "\u0a4b\u0a41"  # ੁੋ vs  ੋੁ
        True
    """

    """
    Nukta is essential to form a new base letter and must be ordered first.

    Udaat, Yakash, and subjoined letters should follow.

    Subjoined letters are constructed (they are not single char), so they cannot be used in the same regex group pattern. See further below for subjoined letters.
    """
    BASE_LETTER_MODIFIERS = [
        "਼",
        "ੑ",
        "ੵ",
    ]

    """
    More generally, when a consonant or independent vowel is modified by multiple vowel signs, the sequence of the vowel signs in the underlying representation of the text should be: left, top, bottom, right.

    p. 491 of The Unicode® Standard Version 14.0 – Core Specification

    https://www.unicode.org/versions/Unicode14.0.0/ch12.pdf
    """
    VOWEL_ORDER = [
        "ਿ",
        "ੇ",
        "ੈ",
        "ੋ",
        "ੌ",
        "ੁ",
        "ੂ",
        "ਾ",
        "ੀ",
    ]

    """
    The remaining diacritics are to be sorted at the end according to the following order
    """
    REMAINING_MODIFIER_ORDER = [
        "ਁ",
        "ੱ",
        "ਂ",
        "ੰ",
        "ਃ",
    ]

    """
    If subjoined were single code points, we could have done a simple regex match:
    ([  list_of_diacritics  ]+)

    Since otherwise, surrounds each lookup of a subjoined letter with lookups of the rest of the diacritics (which are single char).

    The patterns for the single-chars and the subjoined letters:
    """
    GENERATED_MARKS = "".join(
        BASE_LETTER_MODIFIERS + VOWEL_ORDER + REMAINING_MODIFIER_ORDER
    )
    MARK_PATTERN = f"([{GENERATED_MARKS}]*)"

    VIRAMA = "੍"
    BELOW_BASE_LETTERS = "ਹਰਵਟਤਨਚ"
    BELOW_BASE_PATTERN = f"({VIRAMA}[{BELOW_BASE_LETTERS}])?"

    """
    The following regex will capture all sequential diacritics containing at most one subjoined letter.
        >>> print(REGEX_MATCH_PATTERN)
        '([਼ੵਿੇੈੋੌੁੂਾੀਁੱਂੰਃ]*)(੍[ਹਰਵਟਤਨਚ])?([਼ੵਿੇੈੋੌੁੂਾੀਁੱਂੰਃ]*)'
    """
    REGEX_MATCH_PATTERN = f"{MARK_PATTERN}{BELOW_BASE_PATTERN}{MARK_PATTERN}"

    """
    This generates a string of the order in which all diacritics should appear.
        >>> print(GENERATED_MATCH_ORDER)
        '਼ਹਰਵਟਤਨਚਿੇੈੋੌੁੂਾੀਁੱਂੰਃ'
   """
    GENERATED_MATCH_ORDER = "".join(
        BASE_LETTER_MODIFIERS
        + [VIRAMA]
        + [BELOW_BASE_LETTERS]
        + VOWEL_ORDER
        + REMAINING_MODIFIER_ORDER
    )

    def regex_sort_func(match: Match) -> str:
        """
        This re-arranges characters in "match" according to a custom sort order "GENERATED_MATCH_ORDER"
        """
        if len(_match := match.group()) > 1:
            _match = sorted(_match, key=lambda e: GENERATED_MATCH_ORDER.index(e))
            _match = "".join(_match)

        return _match

    string = re.sub(
        REGEX_MATCH_PATTERN,
        regex_sort_func,
        string,
    )

    return string


def sanitize_unicode(string: str) -> str:
    """
    Use single char representations of constructed characters.
    """

    UNICODE_SANITIZATION_MAP = {
        "\u0a73\u0a4b": "\u0a13",  # ਓ
        "\u0a05\u0a3e": "\u0a06",  # ਅ + ਾ = ਆ
        "\u0a72\u0a3f": "\u0a07",  # ਇ
        "\u0a72\u0a40": "\u0a08",  # ਈ
        "\u0a73\u0a41": "\u0a09",  # ਉ
        "\u0a73\u0a42": "\u0a0a",  # ਊ
        "\u0a72\u0a47": "\u0a0f",  # ਏ
        "\u0a05\u0a48": "\u0a10",  # ਐ
        "\u0a05\u0a4c": "\u0a14",  # ਔ
        "\u0a32\u0a3c": "\u0a33",  # ਲ਼
        "\u0a38\u0a3c": "\u0a36",  # ਸ਼
        "\u0a59\u0a3c": "\u0a59",  # ਖ਼
        "\u0a5a\u0a3c": "\u0a5a",  # ਗ਼
        "\u0a5b\u0a3c": "\u0a5b",  # ਜ਼
        "\u0a5e\u0a3c": "\u0a5e",  # ਫ਼
        "\u0a71\u0a02": "\u0a01",  # ਁ adak bindi (quite literally never used today or in the Shabad OS Database, only included for parity with the Unicode block)
    }

    for key, value in UNICODE_SANITIZATION_MAP.items():
        string = string.replace(key, value)

    return string


def decode_unicode(string: str) -> list:
    """
    Takes a string and returns a list of keys and values of each character and its corresponding code point.

    Arg:
        string: The string to affect.

    Returns:
        A list of each character and its corresponding code point.

    Example:
        >>> decode_unicode("To ਜੀ")
        [{'T': '0054'}, {'o': '006f'}, {' ': '0020'}, {'ਜ': '0a1c'}, {'ੀ': '0a40'}]
    """

    return [{item: format(ord(item), "04x")} for item in string]


def encode_unicode(strings: list) -> list:
    """
    Takes a string and returns its corresponding unicode character.

    Arg:
        strings: The list containing any strings to encode.

    Returns:
        A list of any corresponding unicode characters.

    Examples:
        >>> encode_unicode(["0054"])
        'T'

        >>> encode_unicode(["0a1c", "0A40"])
        '['ਜ', 'ੀ']'
    """

    return [chr(int(string, 16)) for string in strings]
