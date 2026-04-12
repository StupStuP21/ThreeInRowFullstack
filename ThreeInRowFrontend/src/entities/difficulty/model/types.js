import PropTypes from 'prop-types';

export const DIFFICULTY_NAMES = {
    EASY: 'Легкий',
    MEDIUM: 'Средний',
    HARD: 'Сложный',
    CUSTOM: 'Кастомный',
};

export const DifficultyPropType = PropTypes.shape({
    difficulty_name: PropTypes.oneOf(Object.values(DIFFICULTY_NAMES)).isRequired,
    row_count_default: PropTypes.oneOfType([PropTypes.number, PropTypes.oneOf([null])]),
    col_count_default: PropTypes.oneOfType([PropTypes.number, PropTypes.oneOf([null])]),
    target_score_default: PropTypes.oneOfType([PropTypes.number, PropTypes.oneOf([null])]),
    game_items_count_default: PropTypes.oneOfType([PropTypes.number, PropTypes.oneOf([null])]),
    is_one_swap_mode_default: PropTypes.oneOfType([PropTypes.bool, PropTypes.oneOf([null])]),
    is_one_item_mode_default: PropTypes.oneOfType([PropTypes.bool, PropTypes.oneOf([null])]),
    id: PropTypes.number.isRequired,
    created_at: PropTypes.string.isRequired,
    updated_at: PropTypes.string.isRequired,
});

export const defaultDifficulty = {
    difficulty_name: DIFFICULTY_NAMES.CUSTOM,
    row_count_default: null,
    col_count_default: null,
    target_score_default: null,
    game_items_count_default: null,
    is_one_swap_mode_default: null,
    is_one_item_mode_default: null,
    id: 0,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
};