import {Layout, theme} from "antd";
import {useParams} from "react-router-dom";
import {GameWidget} from "../../../widgets/game-widget";
import {HeaderContent} from "../../../shared/ui/header/HeaderContent.jsx"
import {FooterContent} from "../../../shared/ui/footer/FooterContent.jsx";

const {Header, Content, Footer} = Layout;

export function GamePage() {
    const {gameId} = useParams();
    const {
        token: {colorBgContainer, borderRadiusLG},
    } = theme.useToken();
    return (
        <Layout style={{minHeight: '100vh'}}>
            <Header style={{marginTop: 0}}>
                <HeaderContent is_create_page={false}></HeaderContent>
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
                <GameWidget gameId={gameId}></GameWidget>
            </Content>
            <Footer style={{textAlign: 'center', marginBottom: 0}} theme="dark">
                <FooterContent />
            </Footer>
        </Layout>
    );
}