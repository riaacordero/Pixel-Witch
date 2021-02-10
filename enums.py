"""
This module contains enum classes used to make the code easier to understand.
"""

from enum import Enum

class PlayerState(Enum):
    """
    Current player state of the game
    """

    LOST = -1
    """Player has died from enemies."""
    ALIVE = 0
    """Player is still continuing to explore the level."""
    WON = 1
    """Player has finished the level by acquiring the key and going to the portal."""


class ColorState(Enum):
    """
    State of the player based on the Potion they consumed. Except the default value WHITE,
    each ColorState gives the player a unique ability, accessible by pressing SPACE.
    """

    WHITE = 0
    """Default color state of the player."""
    RED = 1
    """Player can use a one-time use shield that can less a few seconds."""
    BLUE = 2
    """Player can jump."""
    YELLOW = 3
    """Player can cast a horizontal projectile attack based on the direction they are facing."""


class Location(Enum):
    """
    Used to identify the current menu or place being displayed on the game window.
    """

    PAUSE = -2
    LEVEL_SELECTION = -1
    MAIN_MENU = 0
    LEVEL_ONE = 1
    LEVEL_TWO = 2
    LEVEL_THREE = 3