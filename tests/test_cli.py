import sys
from unittest.mock import MagicMock

import pytest

from affine_cipher import cli


def test_encrypt_dispatch(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(sys, "argv", ["affine-cipher", "encrypt"])

    mock_run_encrypt = MagicMock()

    monkeypatch.setattr(cli, "run_encrypt", mock_run_encrypt)

    cli.main()

    assert mock_run_encrypt.called


def test_decrypt_dispatch(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(sys, "argv", ["affine-cipher", "decrypt"])

    mock_run_decrypt = MagicMock()

    monkeypatch.setattr(cli, "run_decrypt", mock_run_decrypt)

    cli.main()

    assert mock_run_decrypt.called


def test_missing_subcommand(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(sys, "argv", ["affine-cipher"])

    with pytest.raises(SystemExit):
        cli.main()


def test_invalid_subcommand(monkeypatch: pytest.MonkeyPatch) -> None:

    monkeypatch.setattr(sys, "argv", ["affine-cipher", "foo"])

    with pytest.raises(SystemExit):
        cli.main()
