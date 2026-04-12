import copy
import datetime

import numpy as np

from src.enums import MatchTypeEnum, SwapDirectionEnum
from src.exceptions.exceptions import IncorrectGameItemException, IncorrectSwapException, NonExistentSwapException, \
    IncorrectGameFieldShapeException, SmallNumberOfGameItemsException, GameOverException


class GameLogic:
    @staticmethod
    def validate_game_playing_state(current_score: int, target_score: int, is_over_state: bool,
                                    lost_of_time_state: bool):
        """
        Валидация, что игра корректна в состоянии игры, а не закончена
        :param current_score: Текущее кол-во игровых очков
        :param target_score: Целевое кол-во очков для победы
        :param is_over_state: Состояние is_over игры
        :param lost_of_time_state: Состояние lost_of_time игры
        :return: True|False
        """
        if current_score >= target_score or is_over_state or lost_of_time_state:
            raise GameOverException(current_score=current_score, target_score=target_score, is_over=is_over_state,
                                    is_out_of_time=lost_of_time_state)

    @staticmethod
    def check_game_item_index_correct(field: list[list[str]], row_indx: int, col_indx: int) -> bool:
        """
        Проверка имеет ли поданное игровое поле позицию [row_indx][col_indx]
        :param field: Игровое поле
        :param row_indx: Номер строки
        :param col_indx: Номер столбца
        :return: True|False
        """
        return 0 <= row_indx < len(field) and 0 <= col_indx < len(field[0])

    @staticmethod
    def check_swap_type_correct(swap_type: str) -> bool:
        """
        Проверка, что было подано корректное наименование свапа. Сверяет со значениями из SwapDirectionEnum
        :param swap_type: Наименование свапа
        :return: True|False
        """
        return swap_type in (
            SwapDirectionEnum.UP.value, SwapDirectionEnum.DOWN.value, SwapDirectionEnum.LEFT.value,
            SwapDirectionEnum.RIGHT.value
        )

    @staticmethod
    def check_items_count_correct(items_count: int) -> bool:
        """
        Проверка, что было подано корректное количество игровых предметов для создания игрового поля
        :param items_count: Количество игровых предметов
        :return: True|False
        """
        return items_count > 2

    @staticmethod
    def check_loose(last_action_time: datetime.datetime) -> bool:
        """
        Проверка на кондицию поражения из-за бездействия в 2 часа
        :param last_action_time: Время последнего действия
        :return: True|False
        """
        return last_action_time < datetime.datetime.now() - datetime.timedelta(hours=2)

    @staticmethod
    def check_win(current_score: int, target_score) -> bool:
        """
        Проверка на кондицию победы по очкам
        :param current_score: Текущее кол-во игровых очков
        :param target_score: Целевое кол-во очков для победы
        :return: True|False
        """
        return current_score >= target_score

    @staticmethod
    def get_game_items(items_count: int) -> list[str]:
        """
        Возвращает список обозначений игровых предметов, что используются в игре\n
        Пример: \n
        ['A', 'B', ..., 'AA', 'AB', ...]
        :param items_count: Кол-во игровых предметов, которые будут использоваться в игре (на поле)
        :return: Список обозначений игровых элементов
        """
        items = []
        for i in range(1, items_count + 1):
            k = i
            s = ""
            while k:
                k -= 1
                s = chr(ord('A') + k % 26) + s
                k //= 26
            items.append(s)
        return items

    @staticmethod
    def get_random_game_item(items_count: int) -> str:
        """
        Возвращает обозначение случайного валидного игрового предмета для игры с items_count игровыми предметами
        (для режима "случайный предмет")
        :param items_count: Кол-во игровых предметов
        :return: Обозначение игрового предмета
        """
        return np.random.choice(GameLogic.get_game_items(items_count=items_count))

    @staticmethod
    def random_generate_field(row_count: int, col_count: int, game_items: list[str]) -> list[list[str]]:
        """
        Возвращает сгенерированное игровое поле без исходных совпадений 3 и более в ряд.
        Может не иметь потенциальных ходов, ведущих к совпадению.
        Пример игрового поля:\n
        ['B', 'A', 'A', 'C', 'A']\n
        ['C', 'A', 'C', 'C', 'A']\n
        ['C', 'C', 'A', 'B', 'C']\n
        ['A', 'C', 'B', 'B', 'C']\n
        ['C', 'A', 'B', 'C', 'A']\n
        ['C', 'B', 'A', 'C', 'C']\n

        :exception IncorrectGameFieldShapeException: Недопустимые размеры игрового поля

        :param row_count: Кол-во строк игрового поля
        :param col_count: Кол-во столбцов игрового поля
        :param game_items: Список игровых предметов, что используются в игре
        :return: Новое игровое поле
        """
        if row_count + col_count < 6:
            raise IncorrectGameFieldShapeException(row_num=row_count, col_num=col_count)
        field = np.full((row_count, col_count), '-', dtype=str)

        for i in range(row_count):
            for j in range(col_count):
                # Определяем запрещённые значения из-за горизонтального и вертикального совпадения
                forbidden = []

                # Проверяем два слева (если есть)
                if j >= 2 and field[i, j - 1] == field[i, j - 2]:
                    forbidden.append(field[i, j - 1])

                # Проверяем два сверху (если есть)
                if i >= 2 and field[i - 1, j] == field[i - 2, j]:
                    forbidden.append(field[i - 1, j])

                # Допустимые значения
                allowed = [x for x in game_items if x not in forbidden]
                field[i, j] = np.random.choice(allowed)
        return field.tolist()

    @staticmethod
    def create_starting_field(row_count: int, col_count: int, items_count: int, is_one_swap_mode: bool):
        """
        Возвращает сгенерированное игровое поле без исходных совпадений 3 и более в ряд.
        А также поле обязательно имеет потенциальные ходы, ведущие к совпадению.\n
        Пример игрового поля:\n
        ['B', 'A', 'A', 'C', 'A']\n
        ['C', 'A', 'C', 'C', 'A']\n
        ['C', 'C', 'A', 'B', 'C']\n
        ['A', 'C', 'B', 'B', 'C']\n
        ['C', 'A', 'B', 'C', 'A']\n
        ['C', 'B', 'A', 'C', 'C']\n

        :exception SmallNumberOfGameItemsException: Маленькое кол-во игровых предметов

        :param row_count: Кол-во строк игрового поля
        :param col_count: Кол-во столбцов игрового поля
        :param items_count: Кол-во игровых предметов, которые будут использоваться в игре (на поле)
        :param is_one_swap_mode: Активен ли режим "одним свапом"
        :param matched_item: Игровой предмет за который начисляются очки (для режима "случ. предмет")
        :return: Новое игровое поле
        """
        if not GameLogic.check_items_count_correct(items_count=items_count):
            raise SmallNumberOfGameItemsException(items_count=items_count)
        game_items = GameLogic.get_game_items(items_count=items_count)
        while True:
            field = GameLogic.random_generate_field(row_count=row_count, col_count=col_count, game_items=game_items)
            if not GameLogic.check_has_matches_from_field(field=field):
                if GameLogic.check_has_potential_moves(field=field, is_one_swap_mode=is_one_swap_mode):
                    break
        return field

    @staticmethod
    def swap(field: list[list[str]], row_num: int, col_num: int, swap_type: str) -> list[list[str]]:
        """
        Возвращает игровое поле, на котором произведен свап игрового элемента

        :exception IncorrectGameItemException: В функцию был подан несуществующий игровой объект (по позиции)
        :exception IncorrectSwapException: Для данного игрового предмета нельзя произвести данный свап
         (например: для крайнего левого предмета нельзя сделать свап влево)
        :exception NonExistentSwapException: Попытка не существующего свапа
         (значение swap_type не матчится с SwapDirectionEnum)

        :param field: Игровое поле
        :param row_num: Строка игрового элемента перед свапом (позиция)
        :param col_num: Столбец игрового элемента перед свапом (позиция)
        :param swap_type: Тип свапа: left(влево)|right(вправо)|up(вверх)|down(вниз)
        :return: Игровое поле после свапа
        """
        if not GameLogic.check_swap_type_correct(swap_type=swap_type):
            raise NonExistentSwapException(swap_type=swap_type)
        swapped_elem = (
            row_num + 1 \
                if swap_type == SwapDirectionEnum.DOWN.value \
                else row_num - 1 if swap_type == SwapDirectionEnum.UP.value \
                else row_num,
            col_num + 1 \
                if swap_type == SwapDirectionEnum.RIGHT.value \
                else col_num - 1 if swap_type == SwapDirectionEnum.LEFT.value \
                else col_num
        )
        field_temp = copy.deepcopy(field)
        if not GameLogic.check_game_item_index_correct(field=field, row_indx=row_num, col_indx=col_num):
            raise IncorrectGameItemException(row_num=row_num, col_num=col_num)
        elif not GameLogic.check_game_item_index_correct(field=field, row_indx=swapped_elem[0],
                                                         col_indx=swapped_elem[1]):
            raise IncorrectSwapException(row_num=row_num, col_num=col_num, swap_type=swap_type)
        else:
            field_temp[row_num][col_num], field_temp[swapped_elem[0]][swapped_elem[1]] = field_temp[swapped_elem[0]][
                swapped_elem[1]], \
                field_temp[row_num][col_num]
        return field_temp

    @staticmethod
    def get_matches_by_type(field: list[list[str]], type: MatchTypeEnum = MatchTypeEnum.HORIZONTAL,
                            matched_item: str = None) -> dict:
        """
        Возвращает все возможные совпадения 3 и более в ряд на полученном игровом поле
        (для конкретного типа совпадений: горизонтальный | вертикальный) в формате:\n
        {
            'Тип стака (horizontal | vertical)': [
                {
                    'row_num': Номер строки текущего игрового предмета (int, с нуля),\n
                    'col_num': Номер столбца текущего игрового предмета (int, с нуля),\n
                    'value': Число матчей влево | вверх от текущего предмета (int, текущий предмет не считается),\n
                    'is_scoring': True|False (bool, начисляются за данный матч очки)\n
                }
            ]
        }
        :param field: Игровое поле
        :param type: Тип стаков (горизонтальные или вертикальные)
        :param matched_item: Игровой предмет за который начисляются очки (для режима "случ. предмет")
        :return: Выдаёт dict матчей (2 и более стаков) для каждого подходящего предмета
        """
        field_arr = np.array(field)
        matches = {type.value: []}
        horizontal_type_cond = type == MatchTypeEnum.HORIZONTAL.value
        for indx in range(field_arr.shape[0 if horizontal_type_cond else 1]):
            match_counter = 0
            for item_num in range(field_arr.shape[1 if horizontal_type_cond else 0] - 1):
                if field_arr[
                    indx if horizontal_type_cond else item_num,
                    item_num if horizontal_type_cond else indx
                ] == field_arr[
                    indx if horizontal_type_cond else item_num + 1,
                    item_num + 1 if horizontal_type_cond else indx
                ]:
                    match_counter += 1
                else:
                    match_counter = 0
                if match_counter >= 2:
                    matches[type.value].append(
                        {
                            'row_num': indx if horizontal_type_cond else item_num + 1,
                            'col_num': item_num + 1 if horizontal_type_cond else indx,
                            'value': match_counter,
                            'is_scoring': field_arr[indx if horizontal_type_cond else item_num][
                                              item_num if horizontal_type_cond else indx] == matched_item if matched_item else True
                        }
                    )
        return matches

    @staticmethod
    def get_all_matches(field: list[list[str]], matched_item: str = None) -> dict:
        """
        Возвращает все возможные совпадения 3 и более в ряд на полученном игровом поле в формате:\n
        {
            'horizontal': [
                {
                    'row_num': Номер строки текущего игрового предмета (int, с нуля),\n
                    'col_num': Номер столбца текущего игрового предмета (int, с нуля),\n
                    'value': Число матчей влево от текущего предмета (int, текущий предмет не считается),\n
                    'is_scoring': True|False (bool, начисляются ли за данное совпадение очки)\n
                }
            ],
            'vertical': [
                {
                    'row_num': Номер строки текущего игрового предмета (int, с нуля),\n
                    'col_num': Номер столбца текущего игрового предмета (int, с нуля),\n
                    'value': Число матчей вверх от текущего предмета (int, текущий предмет не считается),\n
                    'is_scoring': True|False (bool, начисляются ли за данное совпадение очки)\n
                }
            ]
        }
        :param field: Игровое поле
        :param matched_item: Игровой предмет за который начисляются очки (для режима "случ. предмет")
        :return: Выдаёт dict матчей (2 и более стаков) для каждого подходящего предмета на поле

        """
        all_matches = GameLogic.get_matches_by_type(field=field, type=MatchTypeEnum.HORIZONTAL,
                                                    matched_item=matched_item) \
                      | \
                      GameLogic.get_matches_by_type(field=field, type=MatchTypeEnum.VERTICAL, matched_item=matched_item)
        return all_matches

    @staticmethod
    def check_has_matches_from_all_matches(matches: dict):
        return any(
            list(
                map(lambda x: len(x) > 0, matches.values())
            )
        )

    @staticmethod
    def check_has_matches_from_field(field: list[list[str]], matched_item: str = None) -> bool:
        """
        Проверка на наличие на полученном игровом поле совпадений 3 и более в ряд
        :param field: Игровое поле
        :param matched_item: Игровой предмет за который начисляются очки (для режима "случ. предмет")
        :return: True|False
        """
        return any(
            list(
                map(lambda x: len(x) > 0, GameLogic.get_all_matches(field=field, matched_item=matched_item).values())
            )
        )

    @staticmethod
    def check_has_potential_moves_by_type(field: list[list[str]], is_one_swap_mode: bool,
                                          match_type: MatchTypeEnum) -> bool:
        """
        Проверяет наличие на данном игровом поле ходов (или связки ходов, если не режим "одним свапом"),
        ведущих совпадению 3 и более в ряд, для конкретного типа совпадения (горизонтальный|вертикальный)
        :param field: Игровое поле
        :param is_one_swap_mode: Активен ли режим одним свапом или нет
        :param match_type: Тип совпадения: horizontal(горизонтальный)|vertical(вертикальный)
        :return: True|False
        """
        horizontal_type_cond = match_type == MatchTypeEnum.HORIZONTAL
        field_arr = np.array(field)
        if is_one_swap_mode:
            for indx in range(field_arr.shape[0 if horizontal_type_cond else 1]):
                for item_num in range(field_arr.shape[1 if horizontal_type_cond else 0]):
                    try:
                        if GameLogic.check_has_matches_from_field(
                                field=GameLogic.swap(
                                    field=field,
                                    row_num=indx if horizontal_type_cond else item_num,
                                    col_num=item_num if horizontal_type_cond else indx,
                                    swap_type=SwapDirectionEnum.RIGHT if horizontal_type_cond else SwapDirectionEnum.UP)
                        ):
                            return True
                    except IncorrectSwapException:
                        assert True

                    try:
                        if GameLogic.check_has_matches_from_field(
                                field=GameLogic.swap(
                                    field=field,
                                    row_num=indx if horizontal_type_cond else item_num,
                                    col_num=item_num if horizontal_type_cond else indx,
                                    swap_type=SwapDirectionEnum.LEFT if horizontal_type_cond else SwapDirectionEnum.DOWN)
                        ):
                            return True
                    except IncorrectSwapException:
                        assert True
            return False
        else:
            return len(np.where(np.unique_counts(field_arr).counts >= 3)[0]) > 0

    @staticmethod
    def check_has_potential_moves(field: list[list[str]], is_one_swap_mode: bool) -> bool:
        """
        Проверяет наличие на данном игровом поле ходов (или связки ходов, если не режим "одним свапом"),
        ведущих совпадению 3 и более в ряд
        :param field: Игровое поле
        :param is_one_swap_mode: Активен ли режим одним свапом или нет
        :return: True|False
        """
        if GameLogic.check_has_potential_moves_by_type(field=field, is_one_swap_mode=is_one_swap_mode,
                                                       match_type=MatchTypeEnum.HORIZONTAL):
            return True
        else:
            return GameLogic.check_has_potential_moves_by_type(field=field, is_one_swap_mode=is_one_swap_mode,
                                                               match_type=MatchTypeEnum.VERTICAL)

    @staticmethod
    def mark_matches_on_field(field: list[list[str]], matches: dict) -> list[list[str]]:
        """
        Маркирует, какие элементы на поле должны быть удалены с помощью (True|False). За True очки начисляются,
        за False - нет (для режима "случайный предмет") \n
        Пример:
            ['B', 'A', 'A', 'C', 'A'] \n
            ['C', 'A', 'C', 'C', 'A'] \n
            ['A', 'C', 'A', 'B', 'C'] \n
            [True, 'C', 'B', 'B', 'C'] \n
            [True, 'A', 'B', 'C', 'A'] \n
            [True, 'B', 'A', 'C', 'C'] \n
        :param field: Игровое поле
        :param matches: Все совпадения, что были найдены на данном поле
        :return: Промаркированное игровое поле (элементы для удаления маркируются как True|False)
        """
        for match_type, matches_arr in matches.items():
            for matches in matches_arr:
                for i in range(matches['value'] + 1):
                    row_indx = matches['row_num'] if match_type == MatchTypeEnum.HORIZONTAL.value else matches[
                                                                                                           'row_num'] - i
                    col_indx = matches['col_num'] - i if match_type == MatchTypeEnum.HORIZONTAL.value else matches[
                        'col_num']
                    field[row_indx][col_indx] = matches['is_scoring']
        return field

    @staticmethod
    def get_all_item_indexes_to_delete(marked_field: list[list[str]]) -> list[list[int]]:
        """
        :param marked_field: Промаркированное для удаления предметов поле
        :return: Массив индексов элементов, которые будут удалены
        """
        return [
            [index_row, index_col] for index_row, row in enumerate(marked_field)
            for index_col, item in enumerate(row) if (item is True) or (item is False)
        ]

    @staticmethod
    def get_all_falls(marked_field: list[list[str]]) -> list[list[int]]:
        """
        Возвращает массив с только имеющими падения элементами
        :param marked_field: Промаркированное для удаления предметов поле
        :return: [[номер строки элемента, номер столбца элемента, количество ячеек падения вниз данного элемента],]
        """
        items_to_fall = [
            [index_row, index_col, 0] for index_row, row in enumerate(marked_field)
            for index_col, item in enumerate(row) if (item is not True) and (item is not False)
        ]
        for col_index in range(len(marked_field[0])):
            for row_index in range(len(marked_field)):
                if (marked_field[row_index][col_index] is True) or (marked_field[row_index][col_index] is False):
                    items_to_fall = [
                        [
                            item[0],
                            item[1],
                            item[2] + 1 if (item[1] == col_index and item[0] < row_index) else item[2]
                        ]
                        for item in items_to_fall
                    ]
        return [item for item in items_to_fall if item[2] != 0]

    @staticmethod
    def get_all_spawns(marked_field: list[list[str]]) -> list[list[int]]:
        """
        Возвращает индексы всех элементы, которые должны заспавниться, после удаления элементов
        :param marked_field:
        :return: [[номер строки элемента, номер столбца элемента],]
        """
        items_to_spawn = []
        for col_index in range(len(marked_field[0])):
            count_non_destroy = 0
            for row_index in range(len(marked_field)):
                if (marked_field[row_index][col_index] is True) or (marked_field[row_index][col_index] is False):
                    items_to_spawn.extend([[i, col_index] for i in range(row_index - count_non_destroy + 1)])
                else:
                    count_non_destroy += 1
        res = []
        [res.append(item) for item in items_to_spawn if item not in res]
        return res

    @staticmethod
    def calculate_score(marked_field: list[list[str]]) -> int:
        """
        Счёт очков, полученных за удаление текущих совпадений 3 и более в ряд
        :param marked_field: Промаркированное для удаления предметов поле
        :return: Число очков
        """
        return int(np.count_nonzero(np.array(marked_field) == 'True'))

    @staticmethod
    def apply_score_penalty(current_score: int, penalty: int) -> int:
        """
        Применение штрафа к игровым очкам
        :param current_score: Текущее кол-во игровых очков
        :param penalty: Штраф
        :return: Кол-во очков с учётом штрафа
        """
        return current_score - penalty if current_score - penalty >= 0 else 0

    @staticmethod
    def delete_and_add_new_items_on_field(marked_field: list[list[str]], items_count: int) -> list[list[str]]:
        """
        Удаление элементов, что относятся к матчам 3 и более в ряд. Сдвиг оставшихся элементов вниз,
        соответственно удалениям и добавление новых элементов сверху.
        :param marked_field: Промаркированное для удаления предметов поле
        :param items_count: Кол-во игровых предметов для игры, к которой данное поле относится
        :return: Новое игровое поле, с замененными элементами и сдвигами существующих (если необходимо)
        """
        game_items = GameLogic.get_game_items(items_count=items_count)
        field_arr = np.array(marked_field)
        for row_num in range(len(field_arr)):
            for col_num in range(len(field_arr[row_num])):
                if field_arr[row_num][col_num] == 'True' or field_arr[row_num][col_num] == 'False':
                    field_arr[1:row_num + 1, col_num] = field_arr[0:row_num, col_num]
                    field_arr[0, col_num] = None

        replace_empty_with_new_items_func = np.vectorize(lambda x: np.random.choice(game_items) if x == 'None' else x)

        return replace_empty_with_new_items_func(field_arr).tolist()
