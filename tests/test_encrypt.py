from unittest.mock import MagicMock

import pytest

from affine_cipher.encrypt import affine_encryption, run_encrypt


def test_affine_encryption_with_known_key_hello() -> None:
    result = affine_encryption("HELLO", 3, 10)

    # Assert: check it against what you already hand-verified
    assert result == "FWRRA"


def test_affine_encryption_with_known_key_quartz() -> None:
    result = affine_encryption("QUARTZ", 3, 10)

    assert result == "GSKJPH"


def test_affine_encryption_with_known_key_bollix() -> None:
    result = affine_encryption("BOLLIX", 3, 10)

    assert result == "NARRIB"


def test_affine_encryption_lowercase_passthrough() -> None:
    result = affine_encryption("bollix", 3, 10)

    assert result == "bollix"


def test_affine_encryption_empty_string() -> None:
    result = affine_encryption("", 3, 10)

    assert result == ""


def test_run_encrypt(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:

    mock_input = MagicMock(return_value="HELLO")

    monkeypatch.setattr("builtins.input", mock_input)

    run_encrypt()

    captured = capsys.readouterr()

    assert "FWRRA" in captured.out
