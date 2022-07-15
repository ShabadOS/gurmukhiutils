import re
from typing import Literal, Match

UNICODE_STANDARDS = Literal["Unicode Consortium", "Sant Lipi"]


def unicode(
    string: str,
    unicode_standard: Literal[UNICODE_STANDARDS] = "Unicode Consortium",
) -> str:
    """
    Converts any ascii gurmukhi characters and sanitizes to unicode gurmukhi.

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
    common_ascii_to_unicode_map = {
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
    special_sant_lipi_map = {
        "Î": "\ueeec",  # replace capital i-circumflex letter, half-yayya
        "੍ਯ": "\ueeec",  # replace unicode half-yayya
        "î": "\ueeee",  # i-circumflex letter, open-top half-yayya
        "ï": "\ueeef",  # i-diaeresis letter, open-top full yayya
        "\u2080": "\uee80",  # missing subscript 0 (₀)
        "\u2081": "\uee81",  # subscript 1 (₁) number
        "\u2082": "\uee82",  # subscript 2 (₂) number
        "\u2083": "\uee83",  # subscript 3 (₃) number
        "\u2084": "\uee84",  # subscript 4 (₄) number
        "\u2085": "\uee85",  # subscript 5 (₅) number
        "\u2086": "\uee86",  # subscript 6 (₆) number
        "\u2087": "\uee87",  # missing subscript 7 (₇)
        "\u2088": "\uee88",  # subscript 8 (₈) number
        "\u2089": "\uee89",  # missing subscript 9 (₉)
    }

    sant_lipi_to_unicode_compliant_map = {
        "\ueeec": "੍ਯ",
        "\ueeee": "੍ਯ",
        "\ueeef": "ਯ",
        # The Shabad OS Database as of 2022-06-27 only has these occur before a white-space character:
        "\uee80": "₀",
        "\uee81": "₁",
        "\uee82": "₂",
        "\uee83": "₃",
        "\uee84": "₄",
        "\uee85": "₅",
        "\uee86": "₆",
        "\uee87": "₇",
        "\uee88": "₈",
        "\uee89": "₉",
    }

    # Move ASCII sihari before mapping to unicode
    ascii_base_letters = "a-zA-Z\\|^&Îîï"
    pattern = r"(i)([" + ascii_base_letters + "])"
    string = re.sub(pattern, r"\2\1", string)

    # Replace any ASCII with Unicode Gurmukhi
    for key, value in common_ascii_to_unicode_map.items():
        string = string.replace(key, value)

    for key, value in special_sant_lipi_map.items():
        string = string.replace(key, value)

    # Normalize Unicode
    string = unicode_normalize(string)

    if unicode_standard == "Unicode Consortium":

        # Map Sant Lipi to Unicode Consortium
        for key, value in sant_lipi_to_unicode_compliant_map.items():
            string = string.replace(key, value)

        """
        Fix occurences of half-yayya + diacritic(s)

        This seems to be a major pitfall of the Unicode standard.

        Looks as though using a subjoined character for what is actually a base letter, there is no way to properly add accents / vowels to either the half-y or the letter preceding it.

        Recommendation is to use Sant Lipi standard + font in the mean time.
        """
        string = re.sub("(੍ਯ)([਼੍ੵਿੇੈੋੌੁੂਾੀਁੱਂੰਃ]+)", r"ਯ\2", string)

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
    nukta_udaat_yakash_order_list = [
        "਼",
        "ੑ",
        "ੵ",
    ]

    """
    More generally, when a consonant or independent vowel is modified by multiple vowel signs, the sequence of the vowel signs in the underlying representation of the text should be: left, top, bottom, right.

    p. 491 of The Unicode® Standard Version 14.0 – Core Specification

    https://www.unicode.org/versions/Unicode14.0.0/ch12.pdf
    """
    vowel_order_list = [
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
    remaining_diacritic_order_list = [
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
    generated_single_chars = "".join(
        nukta_udaat_yakash_order_list
        + vowel_order_list
        + remaining_diacritic_order_list
    )
    d_pattern = "([" + generated_single_chars + "]*)"

    subjoin_constructor = "੍"
    subjoin_consonants = "ਹਰਵਟਤਨਚ"
    s_pattern = "(" + subjoin_constructor + "[" + subjoin_consonants + "])?"

    """
    The following regex will capture all sequential diacritics containing at most one subjoined letter.
        >>> print(regex_match_pattern)
        '([਼ੵਿੇੈੋੌੁੂਾੀਁੱਂੰਃ]*)(੍[ਹਰਵਟਤਨਚ])?([਼ੵਿੇੈੋੌੁੂਾੀਁੱਂੰਃ]*)'
    """
    regex_match_pattern = d_pattern + s_pattern + d_pattern

    """
    This generates a string of the order in which all diacritics should appear.
        >>> print(generated_diacritic_order)
        '਼ਹਰਵਟਤਨਚਿੇੈੋੌੁੂਾੀਁੱਂੰਃ'
   """
    generated_diacritic_order = "".join(
        nukta_udaat_yakash_order_list
        + [subjoin_constructor]
        + [subjoin_consonants]
        + vowel_order_list
        + remaining_diacritic_order_list
    )

    def regex_sort_func(match: Match) -> str:
        """
        This re-arranges characters in "match" according to a custom sort order "generated_diacritic_order"
        """
        if len(match := match.group()) > 1:
            match = sorted(match, key=lambda e: generated_diacritic_order.index(e))
            match = "".join(match)

        return match

    string = re.sub(
        regex_match_pattern,
        regex_sort_func,
        string,
    )

    return string


def sanitize_unicode(string: str) -> str:
    """
    Use single char representations of constructed characters.
    """

    unicode_sanitization_map = {
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

    for key, value in unicode_sanitization_map.items():
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
    list = []
    for item in string:
        list.append({item: format(ord(item), "04x")})

    return list


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
    encoded_list = []
    for string in strings:
        encoded_list.append(chr(int(string, 16)))

    return encoded_list
