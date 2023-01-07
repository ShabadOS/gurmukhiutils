from typing import Literal

# from gurmukhiutils.converters.gurmukhi_to_roman_transcript import (
#     gurmukhi_to_roman_transcript,
# )
from gurmukhiutils.converters.gurmukhi_to_roman_translit import (
    gurmukhi_to_roman_translit,
)
from gurmukhiutils.unicode import unicode_normalize

TRANSLATORS = Literal["Gurmukhi to Roman Translit", "Gurmukhi to Roman Transcript"]


def convert(
    string: str,
    scriptConverter: Literal[TRANSLATORS] = "Gurmukhi to Roman Transcript",
) -> str:
    """
    Converts text from a script to another.

    Note:
        Some script converters are lossless and others are lossy. Transliteration attempts to be compliant with reversible mappings (i.e. to a target script and then back to unicode gurmukhi with zero data loss). Transcription attempts to be representative of the spoken word (biased by today's languages).

    Args:
        string: The string to affect.

        scriptConverter: The method of converting one script to another . Defaults to "Gurmukhi to Roman Transcript".

    Returns:
        A string where a script is converted to another script.

    Examples:
        >>> convert("੧੨੩")
        '123'

        >>> convert("ਗੁਰੂ")
        'gurū'
    """

    # Convert Unicode to Sant Lipi format
    string = string.replace("੍ਯ", "꠳ਯ")

    string = unicode_normalize(string)

    if scriptConverter == "Gurmukhi to Roman Translit":
        string = gurmukhi_to_roman_translit(string)

    # if scriptConverter == "Gurmukhi to Roman Transcript":
    # string = gurmukhi_to_roman_transcript(string)

    return string
