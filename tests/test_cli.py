
import pytest
import sys
from affine_cipher import cli
from unittest.mock import MagicMock

def test_encrypt_dispatch(monkeypatch):

    patched_encrypt = monkeypatch.setattr(sys, "argv", ["affine-cipher", "encrypt"])

    mock_run_encrypt = MagicMock()

    patched_cli_run_encrypt = monkeypatch.setattr(cli, "run_encrypt", mock_run_encrypt)

    cli.main()

    assert mock_run_encrypt.called

def test_decrypt_dispatch(monkeypatch):
    
    patched_decrypt = monkeypatch.setattr(sys, "argv",  ["affine-cipher", "decrypt"])

    mock_run_decrypt = MagicMock()

    patched_cli_run_decrypt = monkeypatch.setattr(cli, "run_decrypt", mock_run_decrypt)

    cli.main()

    assert mock_run_decrypt.called

def test_missing_subcommand(monkeypatch):

    patched_missing_subcommand = monkeypatch.setattr(sys, "argv", ["affine-cipher"])

    with pytest.raises(SystemExit):

        cli.main()

def test_invalid_subcommand(monkeypatch):

    patched_invalid_subcommand = monkeypatch.setattr(sys, "argv", ["affine-cipher", "foo"])

    with pytest.raises(SystemExit):

        cli.main()
