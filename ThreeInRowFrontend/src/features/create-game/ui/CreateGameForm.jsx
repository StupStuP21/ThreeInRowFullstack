import {Button, Checkbox, Form, Divider, Radio, Spin, message} from 'antd';
import {InputNumber} from 'antd';
import {useState} from "react";
import {getCustomDifficulty, getDifficultyById} from "../../../entities/difficulty/api/difficultiesApi.js";
import {useNavigate} from "react-router-dom";
import {postGame} from "../../../entities/game/api/gamesApi.js";
import PropTypes from "prop-types";
import {DifficultyPropType} from "../../../entities/difficulty/model/types.js";

const customDifficultyId = await getCustomDifficulty();

const sharedProps = {
    mode: 'spinner',
    min: 1,
    max: 100,
    style: {width: 150},
};

export function CreateGameForm ({difficulties, loading}) {
    const navigate = useNavigate();
    const [form] = Form.useForm();
    const [selectedDifficulty, setSelectedDifficulty] = useState(null);
    const [gameItemsFieldDisabled, setGameItemsFieldDisabled] = useState(false);

    const onFormFieldsChange = async (e) => {
        form.setFieldsValue({
            game_difficulty: customDifficultyId.id
        });
    };
    const handleDifficultyChange = async (e) => {
        const id = e.target.value;
        setSelectedDifficulty(id);

        try {
            const diff = await getDifficultyById(id);
            if (diff.row_count_default && diff.col_count_default && diff.target_score_default) {
                form.setFieldsValue({
                    num_row: diff.row_count_default,
                    num_col: diff.col_count_default,
                    target_score: diff.target_score_default,
                    num_game_items: diff.game_items_count_default,
                    one_swap_mode: diff.is_one_swap_mode_default,
                    random_item_mode: diff.is_one_item_mode_default
                });
                setGameItemsFieldDisabled(true);
            } else {
                setGameItemsFieldDisabled(false);
            }
        } catch (error) {
            message.error('Не удалось загрузить параметры сложности');
        }
    };

    const handleFinish = async (values) => {
        const created_game = await postGame(values);
        navigate(`/game/${created_game.id}`);
    };

    const handleFinishFail = (errorInfo) => {
        console.log(errorInfo);
    };

    return (
        <Form
            form={form}
            name="basic"
            labelCol={{span: 10}}
            onFinish={handleFinish}
            onFinishFailed={handleFinishFail}
            autoComplete="off"
            style={{minWidth: '40%'}}
        >
            <Divider>Создание игры</Divider>

            <Form.Item
                label="Уровень сложности"
                name="game_difficulty"
                rules={[{required: true, message: 'Пожалуйста, укажите уровень сложности'}]}
            >
                {loading ? (
                    <Spin/>
                ) : (
                    <Radio.Group onChange={handleDifficultyChange} value={selectedDifficulty}>
                        {difficulties.map((diff) => (
                            <Radio.Button key={diff.id} value={diff.id}>
                                {diff.difficulty_name}
                            </Radio.Button>
                        ))}
                    </Radio.Group>
                )}
            </Form.Item>

            <Form.Item
                label="Кол-во строк"
                name="num_row"
                initialValue={3}
                rules={[{required: true, message: 'Пожалуйста, укажите кол-во строк игрового поля'}]}
            >
                <InputNumber {...sharedProps} onChange={onFormFieldsChange} placeholder="Outlined"/>
            </Form.Item>

            <Form.Item
                label="Кол-во стобцов"
                name="num_col"
                initialValue={3}
                rules={[{required: true, message: 'Пожалуйста, укажите кол-во столбцов игрового поля'}]}
            >
                <InputNumber {...sharedProps} onChange={onFormFieldsChange} placeholder="Outlined"/>
            </Form.Item>

            <Form.Item
                label="Целевое кол-во очков"
                name="target_score"
                initialValue={3}
                rules={[{
                    required: true,
                    message: 'Пожалуйста, укажите кол-во очков, которое необходимо набрать для победы в игре'
                }]}
            >
                <InputNumber {...sharedProps} onChange={onFormFieldsChange} placeholder="Outlined"/>
            </Form.Item>

            <Form.Item
                label="Кол-во игровых предметов"
                name="num_game_items"
                initialValue={6}
                rules={[{
                    required: true,
                    message: 'Пожалуйста, укажите кол-во игровых предметов'
                }]}
            >
                <InputNumber {...sharedProps} disabled={gameItemsFieldDisabled} onChange={onFormFieldsChange}
                             placeholder="Outlined"/>
            </Form.Item>

            <Form.Item
                name="one_swap_mode"
                valuePropName="checked"
                initialValue={false}
                label='Режим "Одним свапом"'
            >
                <Checkbox onChange={onFormFieldsChange}></Checkbox>
            </Form.Item>

            <Form.Item
                name="random_item_mode"
                valuePropName="checked"
                initialValue={false}
                label='Режим "Случайный предмет"'
            >
                <Checkbox onChange={onFormFieldsChange}></Checkbox>
            </Form.Item>

            <Form.Item label={null}>
                <Button type="primary" htmlType="submit">
                    Создать игру
                </Button>
            </Form.Item>
        </Form>
    )
}

CreateGameForm.propTypes = {
    difficulties: PropTypes.arrayOf(DifficultyPropType).isRequired,
    loading: PropTypes.bool.isRequired
};