import PlotArea, { PlotData } from "./plot"
import { useEffect, CSSProperties } from "react"
import CircleLoader from "react-spinners/CircleLoader";

interface ShowAreaProps {
    plots: PlotData[],
    removePlotAt: (data: PlotData) => void,
    loading: boolean,
}

const override: CSSProperties = {
    display: "block",
    margin: "0 auto",
    borderColor: "red",
};

export function ShowArea(props: ShowAreaProps) {
    let SpinnerColor = "#000000";

    var { plots, removePlotAt, loading } = props;

    useEffect(() => {
        removePlotAt = removePlotAt;
    }, [removePlotAt]);


    return <div className="showArea w-screen">
        {plots.map((pdata) => (
            <PlotArea key={`${pdata.id}-${pdata.ts}`} state={pdata} removePlotAt={removePlotAt} />
        ))}
        <div className="p-60">
            <CircleLoader
                color={SpinnerColor}
                loading={loading}
                cssOverride={override}
                size={100}
                aria-label="Loading Spinner"
                data-testid="loader"
            />
        </div>
    </div>
}