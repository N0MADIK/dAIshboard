import PlotArea, { PlotData } from "./plot"
import { useEffect } from "react"

interface ShowAreaProps {
    plots: PlotData[],
    removePlotAt: (index: number) => void
}


export function ShowArea(props: ShowAreaProps) {

    var { plots, removePlotAt } = props;

    useEffect(() => {
        removePlotAt = removePlotAt;
    }, [removePlotAt]);



    return <div className="showArea w-screen">
        {plots.map((pdata) => (
            <PlotArea key={pdata.id} state={pdata} removePlotAt={removePlotAt} />
        ))}
    </div>
}