export default function DelimiterLine({type, boardStyled, style}) {
    return (
        <div
            style={{
                width: type === 'vertical' ? '3px' : '100%',
                height: type === 'vertical' ? '100%' : '3px',
                ...(boardStyled && type === 'horizontal' && {
                    background: 'linear-gradient(to right, #001529, #1f2a44, #001529)',
                    boxShadow: '0 0 5px rgba(0, 212, 255, 0.4)',
                    marginTop: '1px',
                    marginBottom: '10px',
                }),
                ...(boardStyled && type === 'vertical' && {
                    background: 'linear-gradient(to bottom, #001529, #1f2a44, #001529)',
                    boxShadow: '0 0 5px rgba(0, 212, 255, 0.4)',
                    margin: '0 20px'
                }),
                ...style
            }}
        />
    )
}