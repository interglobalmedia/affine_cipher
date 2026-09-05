from affine_cipher.encrypt import affine_encryption

def test_affine_encryption_with_known_key_hello():
    result = affine_encryption("HELLO", 3, 10)

    # Assert: check it against what you already hand-verified
    assert result == "FWRRA"

def test_affine_encryption_with_known_key_quartz():
    result = affine_encryption("QUARTZ", 3, 10)

    assert result == "GSKJPH"

def test_affine_encryption_with_known_key_bollix():
    result = affine_encryption("BOLLIX", 3, 10)

    assert result == "NARRIB"

def test_affine_encryption_lowercase_passthrough():
    result = affine_encryption("bollix", 3, 10)

    assert result == "bollix"

def test_affine_encryption_empty_string():
    result = affine_encryption("", 3, 10)

    assert result == ""


