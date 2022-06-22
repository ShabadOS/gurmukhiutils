def test_strip():
    from gurmukhiutils.strip import strip
    from gurmukhiutils.constants import (
        VISHRAM_HEAVY,
        VISHRAM_LIGHT,
        VISHRAM_MEDIUM,
        VISHRAMS,
    )

    remove_vishrams_assertions = {
        "Anhd sbd vjwey, hir jIau Gir Awey; hir gux gwvhu nwrI ]": "Anhd sbd vjwey hir jIau Gir Awey hir gux gwvhu nwrI ]",
        "Anhd sbd vjwey hir jIau Gir Awey hir gux gwvhu nwrI ]": "Anhd sbd vjwey hir jIau Gir Awey hir gux gwvhu nwrI ]",
    }

    remove_heavy_assertions = {
        "Anhd sbd vjwey, hir jIau Gir Awey; hir gux gwvhu nwrI ]": "Anhd sbd vjwey, hir jIau Gir Awey hir gux gwvhu nwrI ]",
        "ਸਬਦਿ ਮਰੈ. ਸੋ ਮਰਿ ਰਹੈ; ]": "ਸਬਦਿ ਮਰੈ. ਸੋ ਮਰਿ ਰਹੈ ]",
    }

    remove_medium_assertions = {
        "Anhd sbd vjwey, hir jIau Gir Awey; hir gux gwvhu nwrI ]": "Anhd sbd vjwey hir jIau Gir Awey; hir gux gwvhu nwrI ]"
    }

    remove_light_assertions = {
        "Anhd sbd vjwey, hir jIau Gir Awey; hir gux gwvhu nwrI ]": "Anhd sbd vjwey, hir jIau Gir Awey; hir gux gwvhu nwrI ]",
        "ਸਬਦਿ ਮਰੈ. ਸੋ ਮਰਿ ਰਹੈ; ]": "ਸਬਦਿ ਮਰੈ ਸੋ ਮਰਿ ਰਹੈ; ]",
    }

    remove_medium_and_heavy_assertions = {
        "Anhd sbd vjwey, hir jIau Gir Awey; hir gux gwvhu nwrI ]": "Anhd sbd vjwey hir jIau Gir Awey hir gux gwvhu nwrI ]",
        "ਸਬਦਿ ਮਰੈ. ਸੋ ਮਰਿ ਰਹੈ; ]": "ਸਬਦਿ ਮਰੈ. ਸੋ ਮਰਿ ਰਹੈ ]",
    }

    for key, value in remove_vishrams_assertions.items():
        assert strip(key, VISHRAMS) == value

    for key, value in remove_heavy_assertions.items():
        assert strip(key, VISHRAM_HEAVY) == value

    for key, value in remove_medium_assertions.items():
        assert strip(key, VISHRAM_MEDIUM) == value

    for key, value in remove_light_assertions.items():
        assert strip(key, VISHRAM_LIGHT) == value

    for key, value in remove_medium_and_heavy_assertions.items():
        assert strip(key, VISHRAM_MEDIUM, VISHRAM_HEAVY) == value


def test_strip_past():
    from gurmukhiutils.strip import strip_past
    from gurmukhiutils.constants import LINE_ENDING_PATTERNS

    remove_past_line_endings_assertions = [
        "ਸਬਦ ॥ ਰਹਾਉ ॥",
        "ਸਬਦ ॥੧॥ ਰਹਾਉ ॥",
        "ਸਬਦ ॥੧॥ ਰਹਾਉ ਦੂਜਾ ॥",
        "ਸਬਦ ॥੪॥੬॥ ਛਕਾ ੧ ॥",
        "ਸਬਦ ॥੨॥੧੨॥ ਛਕੇ ੨ ॥",
        "ਸਬਦ ।੪੯।੧। ਇਕੁ ।",
        "ਸਬਦ ॥੪॥੯॥ ਦੁਤੁਕੇ",
        "ਸਬਦ ॥੨੧॥੧॥ ਸੁਧੁ ਕੀਚੇ",
        "ਸਬਦ ॥੫੧੭॥ ਪੜ੍ਹੋ ਵੀਚਾਰ ਕਬਿੱਤ ੫੦੬",
        "ਸਬਦ ॥੧॥",
        "ਸਬਦ  ॥੧॥",
        "ਸਬਦ॥੨੦",
        "ਸਬਦ ॥੨॥੨॥",
        "ਸਬਦ ॥ ਰਹਾਉ ਦੂਜਾ ॥੧॥੩॥",
        "ਸਬਦ ।੧੪੮।",
    ]

    for line in remove_past_line_endings_assertions:
        assert strip_past(line, LINE_ENDING_PATTERNS) == "ਸਬਦ"


def test_strip_line_endings():
    from gurmukhiutils.strip import strip_line_endings

    remove_line_endings_assertions = {
        "ਸਬਦ ॥ ਸਬਦ ॥": "ਸਬਦ ਸਬਦ",
        "॥ ਜਪੁ ॥": "ਜਪੁ",
        "ਸੂਰਜੁ; ਏਕੋ ਰੁਤਿ ਅਨੇਕ ॥ ਨਾਨਕ ਕਰਤੇ ਕੇ ਕੇਤੇ ਵੇਸ ॥੨॥੨॥": "ਸੂਰਜੁ; ਏਕੋ ਰੁਤਿ ਅਨੇਕ ਨਾਨਕ ਕਰਤੇ ਕੇ ਕੇਤੇ ਵੇਸ",
        "ਸੋ ਦਰੁ ਰਾਗੁ ਆਸਾ ਮਹਲਾ ੧": "ਸੋ ਦਰੁ ਰਾਗੁ ਆਸਾ ਮਹਲਾ ੧",
        "ਮਹਲਾ ੫": "ਮਹਲਾ ੫",
        "Forever And Ever True. ||1||": "Forever And Ever True.",
        "... lush greenery. ||1||Pause||": "... lush greenery.",
        "Example test ||Pause||": "Example test",
    }

    for key, value in remove_line_endings_assertions.items():
        assert strip_line_endings(key) == value
