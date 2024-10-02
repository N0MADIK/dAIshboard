

import { ShowArea } from "./showArea";
import { Chatbox } from "./chatbox";
import { useParams } from 'react-router-dom'
import { useState, useEffect } from 'react';
import { PlotData } from "./plot"
import { axiosInstance } from "@/lib/utils";



export function Display() {
    const [plots, setPlots] = useState<PlotData[]>([]);
    const { user_id, project_id } = useParams()
    let [loading, setLoading] = useState(false);
    let [error, setError] = useState<string | null>(null);

    const removePlot = () => {
        for (var p of plots) {
            removePlotAt(p);
        }
        setPlots([])
    }

    useEffect(() => {
        axiosInstance.get(`/all_plots/${user_id}/${project_id}`).then((response) => {
            let data = response.data;
            let newPlots = [];
            for (let index = 0; index < data.length; index++) {
                let p = JSON.parse(data[index].json);
                let plot_id = data[index].id;
                p.layout.width = 300;
                p.layout.height = 300;
                let x = p.layout.width * Math.floor(index / 1);
                let y = p.layout.height * (index % 1);
                newPlots.push(
                    {
                        id: `Plot ${plot_id}`,
                        width: p.layout.width,
                        height: p.layout.height,
                        x: x,
                        y: y,
                        data: p.data,
                        layout: p.layout,
                        frames: [],
                        config: {},
                        index: index,
                        ts: Date.now()
                    }
                )

            }
            setPlots(newPlots);
            setError(null);
        })
    }, [])




    const removePlotAt = (data: PlotData) => {
        let plot_id = data.id.split(" ")[1];
        axiosInstance.delete(`/delete_plot/${user_id}/${project_id}/${plot_id}`).then((_response) => {
            let newPlots = plots.map(l => Object.assign({}, l)).filter(item => item.id !== data.id);
            setPlots(newPlots);
        });
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
                    let new_plot_id = `Plot ${plot_id}`
                    let newPlots = plots.map(l => Object.assign({}, l));
                    let exisitng_plot = newPlots.find((p) => { return p.id === new_plot_id })
                    data.layout.width = 300;
                    data.layout.height = 300;
                    let index = plots.length;
                    let x = data.layout.width * Math.floor(index / 1);
                    let y = data.layout.height * (index % 1);
                    console.log("existing plot!!!!", exisitng_plot);
                    if (exisitng_plot !== undefined) {
                        data.layout.width = exisitng_plot.layout.width;
                        data.layout.height = exisitng_plot.layout.height;
                        index = exisitng_plot.index;
                        x = exisitng_plot.x;
                        y = exisitng_plot.y;
                    }

                    newPlots = newPlots.filter((p) => { return p.id !== new_plot_id })
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