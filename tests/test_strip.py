def test_strip_vishrams():
    from gurmukhiutils.strip import strip_vishrams

    assertions = {
        "ਸਬਦ. ਸਬਦ, ਸਬਦ; ਸਬਦ ॥": "ਸਬਦ ਸਬਦ ਸਬਦ ਸਬਦ ॥",
        "sbd, sbd sbd; sbd ]": "sbd sbd sbd sbd ]",
        "sbd sbd sbd ]": "sbd sbd sbd ]",
    }

    for key, value in assertions.items():
        assert strip_vishrams(key) == value


def test_strip_vishram():
    from gurmukhiutils.constants import (
        VISHRAM_HEAVY,
        VISHRAM_LIGHT,
        VISHRAM_MEDIUM,
    )
    from gurmukhiutils.strip import strip

    heavy_assertions = {
        "sbd, sbd sbd; sbd ]": "sbd, sbd sbd sbd ]",
        "ਸਬਦ. ਸਬਦ; ਸਬਦ ਸਬਦ ॥": "ਸਬਦ. ਸਬਦ ਸਬਦ ਸਬਦ ॥",
    }

    medium_assertions = {
        "sbd, sbd sbd; sbd ]": "sbd sbd sbd; sbd ]",
        "ਸਬਦ. ਸਬਦ; ਸਬਦ ਸਬਦ ॥": "ਸਬਦ. ਸਬਦ; ਸਬਦ ਸਬਦ ॥",
    }

    light_assertions = {
        "sbd, sbd sbd; sbd ]": "sbd, sbd sbd; sbd ]",
        "ਸਬਦ. ਸਬਦ; ਸਬਦ ਸਬਦ ॥": "ਸਬਦ ਸਬਦ; ਸਬਦ ਸਬਦ ॥",
    }

    medium_and_heavy_assertions = {
        "sbd, sbd sbd; sbd ]": "sbd sbd sbd sbd ]",
        "ਸਬਦ. ਸਬਦ; ਸਬਦ ਸਬਦ ॥": "ਸਬਦ. ਸਬਦ ਸਬਦ ਸਬਦ ॥",
    }

    for key, value in heavy_assertions.items():
        assert strip(key, VISHRAM_HEAVY) == value

    for key, value in medium_assertions.items():
        assert strip(key, VISHRAM_MEDIUM) == value

    for key, value in light_assertions.items():
        assert strip(key, VISHRAM_LIGHT) == value

    for key, value in medium_and_heavy_assertions.items():
        assert strip(key, [VISHRAM_MEDIUM, VISHRAM_HEAVY]) == value


def test_strip_line_endings():
    from gurmukhiutils.strip import strip_line_endings

    assertions = {
        "ਸਬਦ ॥ ਰਹਾਉ ॥": "ਸਬਦ",
        "ਸਬਦ ॥੧॥ ਰਹਾਉ ॥": "ਸਬਦ",
        "ਸਬਦ ॥੧॥ ਰਹਾਉ ਦੂਜਾ ॥": "ਸਬਦ",
        "ਸਬਦ ॥੪॥੬॥ ਛਕਾ ੧ ॥": "ਸਬਦ",
        "ਸਬਦ ॥੨॥੧੨॥ ਛਕੇ ੨ ॥": "ਸਬਦ",
        "ਸਬਦ ।੪੯।੧। ਇਕੁ ।": "ਸਬਦ",
        "ਸਬਦ ॥੪॥੯॥ ਦੁਤੁਕੇ": "ਸਬਦ",
        "ਸਬਦ ॥੨੧॥੧॥ ਸੁਧੁ ਕੀਚੇ": "ਸਬਦ",
        "ਸਬਦ ॥੫੧੭॥ ਪੜ੍ਹੋ ਵੀਚਾਰ ਕਬਿੱਤ ੫੦੬": "ਸਬਦ",
        "ਸਬਦ ॥੧॥": "ਸਬਦ",
        "ਸਬਦ  ॥੧॥": "ਸਬਦ",
        "ਸਬਦ॥੨੦": "ਸਬਦ",
        "ਸਬਦ ॥੨॥੨॥": "ਸਬਦ",
        "ਸਬਦ ॥ ਰਹਾਉ ਦੂਜਾ ॥੧॥੩॥": "ਸਬਦ",
        "ਸਬਦ ।੧੪੮।": "ਸਬਦ",
        "ਸਬਦ ॥ ਸਬਦ ॥": "ਸਬਦ ਸਬਦ",
        "॥ ਸਬਦ ॥": "ਸਬਦ",
        "ਸਬਦ ॥ ਸਬਦ ॥੨॥੨॥": "ਸਬਦ ਸਬਦ",
        "ਮਹਲਾ ੧": "ਮਹਲਾ ੧",
        "ਮਹਲਾ ੫": "ਮਹਲਾ ੫",
        "Example test. ||1||": "Example test.",
        "Example test. ||1||Pause||": "Example test.",
        "Example test. ||Pause||": "Example test.",
    }

    for key, value in assertions.items():
        assert strip_line_endings(key) == value
