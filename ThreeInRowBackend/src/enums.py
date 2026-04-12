import enum

class DifficultyNameEnum(str, enum.Enum):
    EASY = "Простой"
    NORMAL = "Средний"
    HARD = "Сложный"
    CUSTOM = "Кастомный"

class MatchTypeEnum(str, enum.Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'

class SwapDirectionEnum(str, enum.Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'