import {Menu} from "antd";
import {useLocation, useNavigate} from "react-router-dom";

export function HeaderContent() {
    const navigate = useNavigate();
    const route = useLocation();
    const items = [
        {key: '/create_game', label: 'Создать новую игру'},
        {key: '/leaderboard/1', label: 'Таблица лидеров'}
    ]

    function onClick(e) {
        navigate(`${e.key}`)
    };
    return (
        <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={[route.pathname]}
            items={items}
            onClick={onClick}
            style={{flex: 1, justifyContent: 'flex-end', minWidth: 0}}
        />
    )
}