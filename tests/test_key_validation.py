import pytest

from affine_cipher.key_validation import validate_affine_key


def test_validate_affine_key_valid_coprime() -> None:
    a = 3
    m = 26

    assert validate_affine_key(a, m) is None  # type: ignore[func-returns-value]


def test_validate_affine_key_invalid_coprime() -> None:

    a = 4
    m = 26

    with pytest.raises(ValueError):
        validate_affine_key(a, m)
