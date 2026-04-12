class IncorrectGameItemException(Exception):
    def __init__(self, row_num: int, col_num: int):
        self.row_num = row_num
        self.col_num = col_num

    def __str__(self):
        return f'Game item in position: ({self.row_num}, {self.col_num}) does not exist in this field'


class IncorrectSwapException(Exception):
    def __init__(self, swap_type: str, row_num: int, col_num: int):
        self.swap_type = swap_type
        self.row_num = row_num
        self.col_num = col_num

    def __str__(self):
        return f'Cannot make {self.swap_type} swap for game item on position ({self.row_num}, {self.col_num})'


class NonExistentSwapException(Exception):
    def __init__(self, swap_type: str):
        self.swap_type = swap_type

    def __str__(self):
        return f'{self.swap_type} swap is not exist in game logic'


class IncorrectGameFieldShapeException(Exception):
    def __init__(self, row_num: int, col_num: int):
        self.row_num = row_num
        self.col_num = col_num

    def __str__(self):
        return f'Shape: [{self.row_num}, {self.col_num}] is too small for game. At least 6 cells game field should have'


class SmallNumberOfGameItemsException(Exception):
    def __init__(self, items_count: int):
        self.items_count = items_count

    def __str__(self):
        return f'Game should have more than 2 game items to correctly play. Not {self.items_count}'


class GameOverException(Exception):
    def __init__(self, current_score: int, target_score: int, is_over: bool, is_out_of_time: bool):
        self.current_score = current_score
        self.target_score = target_score
        self.is_over = is_over
        self.is_out_of_time = is_out_of_time

    def __str__(self):
        return f'Trying to make an action in already over game with parameters: current_score: {self.current_score}, target_score: {self.target_score}, is_over: {self.is_over}, lost_of_time: {self.is_out_of_time} is already over.'


class ObjectNotFoundException(Exception):
    def __init__(self, model_name: str, id_: int):
        self.model_name = model_name
        self.id = id_

    def __str__(self):
        return f'{self.model_name} with id={self.id} not found'


allowed_exceptions_list = (IncorrectGameItemException, IncorrectSwapException, NonExistentSwapException,
                           IncorrectGameFieldShapeException, SmallNumberOfGameItemsException, GameOverException,
                           ObjectNotFoundException)
