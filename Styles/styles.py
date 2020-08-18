from typing import List

from typing_extensions import TypedDict


class KeyColors(TypedDict):
    background: str
    text: str


class KeyStates(TypedDict):
    active: KeyColors
    inactive: KeyColors
    onPress: KeyColors
    onHover: KeyColors


class KeyStyle(TypedDict):
    fontFamily: str
    offset: int
    colors: KeyStates


class KeyboardStyle(TypedDict):
    keySize: int
    borderSize: int
    keyStyle: KeyStyle


class Style(TypedDict):
    id: int
    name: str
    keyboardStyle: KeyboardStyle


class Styles(List[Style]):
    pass
