from unittest.mock import MagicMock

import pytest

from affine_cipher.decrypt import (
    affine_brute_force,
    affine_decrypt,
    extended_gcd,
    modular_inverse,
    run_decrypt,
)


def test_affine_decrypt_with_known_key_hello() -> None:

    result = affine_decrypt("FWRRA", 3, 10)

    assert result == "HELLO"


def test_affine_decrypt_with_known_key_bollix() -> None:

    result = affine_decrypt("NARRIB", 3, 10)

    assert result == "BOLLIX"


def test_affine_decrypt_with_known_key_quartz() -> None:

    result = affine_decrypt("GSKJPH", 3, 10)

    assert result == "QUARTZ"


def test_affine_decrypt_lowercase_case_preserved() -> None:

    result = affine_decrypt("narrib", 3, 10)

    assert result == "bollix"


def test_affine_decrypt_empty_string() -> None:

    result = affine_decrypt("", 3, 10)

    assert result == ""


# Function to get the Euclidean Algorithm
def test_extended_gcd_with_valid_input() -> None:

    result = extended_gcd(3, 26)

    assert result == (1, 9, -1)


def test_modular_inverse_with_valid_input() -> None:

    result = modular_inverse(3, 26)

    assert result == 9


def test_modular_inverse_raises_when_no_inverse_exists() -> None:

    with pytest.raises(ValueError):
        modular_inverse(2, 26)


def test_affine_brute_force_finds_correct_key(
    capsys: pytest.CaptureFixture[str],
) -> None:

    affine_brute_force("FWRRA")

    captured = capsys.readouterr()

    assert "Key a=3, b=10: HELLO" in captured.out


def test_run_decrypt(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:

    mock_input = MagicMock(return_value="FWRRA")

    monkeypatch.setattr("builtins.input", mock_input)

    run_decrypt()

    captured = capsys.readouterr()

    assert "Key a=3, b=10: HELLO" in captured.out
