from affine_cipher.decrypt import affine_decrypt, extended_gcd, modular_inverse, affine_brute_force, run_decrypt
from affine_cipher import cli
import pytest
from unittest.mock import MagicMock
from colorama import init, Fore

def test_affine_decrypt_with_known_key_hello():

    result = affine_decrypt("FWRRA", 3, 10)

    assert result == "HELLO"

def test_affine_decrypt_with_known_key_bollix():

    result = affine_decrypt("NARRIB", 3, 10)

    assert result == "BOLLIX"

def test_affine_decrypt_with_known_key_quartz():

    result = affine_decrypt("GSKJPH", 3, 10)

    assert result == "QUARTZ"

def test_affine_decrypt_lowercase_passthrough():

    result = affine_decrypt("bollix", 3, 10)

    assert result == "bollix"

def test_affine_decrypt_empty_string():

    result = affine_decrypt("", 3, 10)

    assert result == ""

# Function to get the Euclidean Algorithm
def test_extended_gcd_with_valid_input():
    
    result = extended_gcd(3, 26)

    assert result == (1, 9, -1)

def test_modular_inverse_with_valid_input():

    result = modular_inverse(3, 26)

    assert result == 9

def test_modular_inverse_raises_when_no_inverse_exists():

    with pytest.raises(Exception):
        modular_inverse(2, 26)

def test_affine_brute_force_finds_correct_key(capsys):

    affine_brute_force("FWRRA")

    captured = capsys.readouterr()

    assert "Key a=3, b=10: HELLO" in captured.out

def test_run_decrypt(capsys, monkeypatch):

    mock_input = MagicMock(return_value="FWRRA")

    monkeypatch.setattr("builtins.input", mock_input)

    run_decrypt()
    
    captured = capsys.readouterr()

    assert "Key a=3, b=10: HELLO" in captured.out
