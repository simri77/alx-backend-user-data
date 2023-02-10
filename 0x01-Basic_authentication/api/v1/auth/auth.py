#!/usr/bin/env python3
"""Module defines the authorization class"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Authorization class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Retricts app access to authorization first"""
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        if path[-1] != '/':
            path += '/'
        for i in excluded_paths:
            if i.endswith('*'):
                if path.startswith(i[:1]):
                    return False
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """Defines the authorization header"""
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        else:
            return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns current user"""
        return None
