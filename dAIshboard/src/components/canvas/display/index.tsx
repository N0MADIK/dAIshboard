

import { ShowArea } from "./showArea";
import { Chatbox } from "./chatbox";
import { useParams } from 'react-router-dom'
import { useState } from 'react';
import { PlotData } from "./plot"
import { axiosInstance } from "@/lib/utils";



export function Display() {
    const [plots, setPlots] = useState<PlotData[]>([]);
    const { user_id, project_id } = useParams()
    let [loading, setLoading] = useState(false);
    let [error, setError] = useState<string | null>(null);

    const removePlot = () => {
        console.log("Remove Plots called");
        setPlots([])
    }

    const removePlotAt = (data: PlotData) => {
        let newPlots = plots.map(l => Object.assign({}, l)).filter(item => item.id !== data.id);
        setPlots(newPlots);
    }



    const addPlot = (query: string) => {
        if (plots.length > 5) {
            setError("Maxmimum allowed plots are 5 please close one to create new");
        }
        setLoading(true)
        const dt = { "user_query": query }
        axiosInstance.post(`/generate_plot/${user_id}/${project_id}`, dt)
            .then((response) => {
                let error_message = response.data.error_message;
                if (error_message != undefined) {
                    setError(error_message);
                } else {
                    let data = JSON.parse(response.data.plot_json);
                    let plot_id = response.data.plot_id;
                    let index = plots.length;
                    let newPlots = plots.map(l => Object.assign({}, l));
                    newPlots = newPlots.filter((p) => { return p.id !== (`Plot ${plot_id}`) })
                    data.layout.width = 300;
                    data.layout.height = 300;
                    let x = data.layout.width * Math.floor(index / 1);
                    let y = data.layout.height * (index % 1);
                    newPlots.push(
                        {
                            id: `Plot ${plot_id}`,
                            width: data.layout.width,
                            height: data.layout.height,
                            x: x,
                            y: y,
                            data: data.data,
                            layout: data.layout,
                            frames: [],
                            config: {},
                            index: index,
                            ts: Date.now()
                        }
                    )
                    setPlots(newPlots);
                    setError(null);
                }
                setLoading(false)
            }).catch((err) => {
                setLoading(false)
                console.error('Error:', err);
            });;
    }


    return <div>
        <div className="flex h-4/5 w-screen bg-slate-500"><ShowArea plots={plots} loading={loading} removePlotAt={removePlotAt} /></div>
        <div className="flex h-1/6 w-screen "><Chatbox error={error} removePlots={removePlot} addPlot={addPlot} /></div>
    </div>

}