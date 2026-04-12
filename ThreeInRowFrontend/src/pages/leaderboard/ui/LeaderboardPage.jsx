import {Layout, theme} from "antd";
import {HeaderContent} from "../../../shared/ui/header/HeaderContent.jsx"
import {FooterContent} from "../../../shared/ui/footer/FooterContent.jsx";
import {LeaderboardWidget} from "../../../widgets/leaderboard-widget/index.js";
import {useParams} from "react-router-dom";

const {Header, Content, Footer} = Layout;

export function LeaderboardPage () {
    const {
        token: {colorBgContainer, borderRadiusLG},
    } = theme.useToken();
    const {difficultyId} = useParams();
    return (
        <Layout style={{minHeight: '100vh'}}>
            <Header style={{marginTop: 0}}>
                <HeaderContent />
            </Header>
            <Content style={{
                margin: '24px 16px',
                padding: 24,
                minHeight: 280,
                background: colorBgContainer,
                borderRadius: borderRadiusLG,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center'
            }}>
                <LeaderboardWidget difficultyId={difficultyId}></LeaderboardWidget>
            </Content>
            <Footer style={{textAlign: 'center', marginBottom: 0}} theme="dark">
                <FooterContent />
            </Footer>
        </Layout>
    )
}