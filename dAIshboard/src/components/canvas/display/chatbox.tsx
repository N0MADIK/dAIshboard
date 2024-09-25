


interface ChatBoxProps {
    removePlots: () => void
    addPlot: () => void
}
export function Chatbox(props: ChatBoxProps) {
    const { removePlots, addPlot } = props;
    return <div>
        <h1>This is chatbox</h1>
        <button onClick={removePlots}
        >Remove All Plots</button>
        <br />
        <button onClick={addPlot}>
            Add New Plot
        </button>
    </div>
}