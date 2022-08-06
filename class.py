"""Inventory abstractions"""

import attrs

@attrs.define
class Laptop:
    """A laptop"""
    ident: str
    cpu: str
