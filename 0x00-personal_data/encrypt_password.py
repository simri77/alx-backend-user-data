#!/usr/bin/env python3
"""
Module encrypt_password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Reterive a salted, hashed password, which is a byte string.
    Parameters
    ----------
    password: str
      password to be hashed
    """
    encode = bytes(password, encoding="utf-8")
    hashed = bcrypt.hashpw(encode, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password matches the hashed password

    Parameters
    ----------
    hashed_password: bytes
        hashed password
    password: str
      password to be hashed
    """
    encode = bytes(password, encoding="utf-8")
    return bcrypt.checkpw(encode, hashed_password)
