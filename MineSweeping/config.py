# -*- coding: utf-8 -*-
from enum import Enum

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class BoardSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

# Default settings
DEFAULT_DIFFICULTY = Difficulty.EASY
DEFAULT_BOARD_SIZE = BoardSize.SMALL

# Board size configurations (keeping aspect ratio more square)
BOARD_SIZES = {
    BoardSize.SMALL: {"width": 9, "height": 9},    # 9x9 is standard beginner size
    BoardSize.MEDIUM: {"width": 16, "height": 16},  # 16x16 is standard intermediate size
    BoardSize.LARGE: {"width": 24, "height": 20}    # Adjusted from 30x16 to 24x20 for better proportions
}

# Mine count configurations (standard percentages)
DIFFICULTY_MINE_PERCENT = {
    Difficulty.EASY: 0.12,    # 12% of cells are mines
    Difficulty.MEDIUM: 0.16,  # 16% of cells are mines
    Difficulty.HARD: 0.20     # 20% of cells are mines
}

# Display settings
SIZE = 30  # Increased block size for better visibility
MENU_WIDTH = 400  # Fixed menu width
MENU_HEIGHT = 600  # Fixed menu height

# Text configurations for different languages
GAME_TEXT = {
    "title": u"踩地雷",
    "difficulty": {
        Difficulty.EASY: u"簡單",
        Difficulty.MEDIUM: u"普通",
        Difficulty.HARD: u"困難"
    },
    "size": {
        BoardSize.SMALL: u"小",
        BoardSize.MEDIUM: u"中",
        BoardSize.LARGE: u"大"
    },
    "start_button": u"開始遊戲",
    "difficulty_prefix": u"難度: ",
    "size_prefix": u"大小: "
}
