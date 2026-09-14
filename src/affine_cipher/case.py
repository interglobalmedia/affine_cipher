def restore_char_case(original: str, transformed: str) -> str:
    if original.islower():
        return transformed.lower()
    else:
        return transformed
