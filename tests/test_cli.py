import sys
from unittest.mock import MagicMock

import pytest

from affine_cipher import cli


def test_encrypt_dispatch(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(
        sys, "argv", ["affine-cipher", "encrypt", "-a", "3", "-b", "10"]
    )

    mock_run_encrypt = MagicMock()

    monkeypatch.setattr(cli, "run_encrypt", mock_run_encrypt)

    cli.main()

    mock_run_encrypt.assert_called_once_with(3, 10)


def test_decrypt_dispatch(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(sys, "argv", ["affine-cipher", "decrypt"])

    mock_run_decrypt = MagicMock()

    monkeypatch.setattr(cli, "run_decrypt", mock_run_decrypt)

    cli.main()

    mock_run_decrypt.assert_called_once_with(None, None, False)


def test_decrypt_dispatch_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(sys, "argv", ["affine-cipher", "decrypt", "-a", "3"])

    with pytest.raises(SystemExit):
        cli.main()


def test_decrypt_dispatch_known_key_only(
    monkeypatch: pytest.MonkeyPatch,
) -> None:

    monkeypatch.setattr(
        sys,
        "argv",
        ["affine-cipher", "decrypt", "-a", "3", "-b", "10"],
    )

    mock_run_decrypt = MagicMock()

    monkeypatch.setattr(cli, "run_decrypt", mock_run_decrypt)

    cli.main()

    mock_run_decrypt.assert_called_once_with(3, 10, False)


def test_missing_subcommand(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(sys, "argv", ["affine-cipher"])

    with pytest.raises(SystemExit):
        cli.main()


def test_invalid_subcommand(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(sys, "argv", ["affine-cipher", "foo"])

    with pytest.raises(SystemExit):
        cli.main()


def test_run_encrypt_side_effect_value_error(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(
        sys, "argv", ["affine-cipher", "encrypt", "-a", "3", "-b", "10"]
    )

    mock_run_encrypt = MagicMock(side_effect=ValueError("some message"))

    monkeypatch.setattr(cli, "run_encrypt", mock_run_encrypt)

    with pytest.raises(SystemExit):
        cli.main()

    mock_run_encrypt.assert_called_once_with(3, 10)


def test_run_decrypt_side_effect_value_error(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(
        sys, "argv", ["affine-cipher", "decrypt", "-a", "3", "-b", "10"]
    )

    mock_run_decrypt = MagicMock(side_effect=ValueError("some message"))

    monkeypatch.setattr(cli, "run_decrypt", mock_run_decrypt)

    with pytest.raises(SystemExit):
        cli.main()

    mock_run_decrypt.assert_called_once_with(3, 10, False)
