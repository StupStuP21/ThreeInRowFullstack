import {Layout, Row, theme} from 'antd';
import {HeaderContent} from "../../../shared/ui/header/HeaderContent.jsx";
import {CreateGameForm} from "../../../features/create-game";
import {useDifficulties} from "../../../entities/difficulty/lib/useDifficulties.js";
import {FooterContent} from "../../../shared/ui/footer/FooterContent.jsx";

const {Header, Content, Footer} = Layout;

export function CreateGamePage() {
    const {difficulties, loading} = useDifficulties();
    const {
        token: {colorBgContainer, borderRadiusLG},
    } = theme.useToken();

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
                <Row type="flex" justify="center" align="middle" style={{minWidth: '100%'}}>
                    <CreateGameForm
                        difficulties={difficulties}
                        loading={loading}
                    />
                </Row>
            </Content>
            <Footer style={{textAlign: 'center', marginBottom: 0}}>
                <FooterContent />
            </Footer>
        </Layout>
    )
}