import math


def validate_affine_key(a: int, m: int) -> None:
    if math.gcd(a, m) != 1:
        compute_valid_key = ", ".join(
            str(i) for i in range(1, m) if math.gcd(i, m) == 1
        )
        raise ValueError(f"This key is invalid. Try again. {compute_valid_key}")
