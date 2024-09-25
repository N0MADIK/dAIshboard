

import { ShowArea } from "./showArea";
import { Chatbox } from "./chatbox";

import axios from 'axios';
import { useState, useRef, useEffect } from 'react';
import { PlotData } from "./plot"


const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000',
});


export function Display() {
    const [plots, setPlots] = useState<PlotData[]>([]);

    const removePlot = () => {
        console.log("Remove Plots called");
        setPlots([])
    }

    const removePlotAt = (data: PlotData) => {
        let newPlots = plots.map(l => Object.assign({}, l)).filter(item => item.index != data.index);
        setPlots(newPlots);
    }



    const addPlot = () => {
        axiosInstance.get(`/plot`)
            .then(({ data }) => {
                let index = plots.length;
                let newPlots = plots.map(l => Object.assign({}, l));
                newPlots.push(
                    {
                        id: `TEST ${index}`,
                        width: data.layout.width,
                        height: data.layout.height,
                        x: 0,
                        y: 0,
                        data: data.data,
                        layout: data.layout,
                        frames: [],
                        config: {},
                        index: index
                    }
                )
                setPlots(newPlots);
            });

    }


    return <div>
        <div className="flex h-3/4 w-screen border-4 border-solid border-indigo-500 bg-slate-500"><ShowArea plots={plots} removePlotAt={removePlotAt} /></div>
        <div className="flex h-1/4 w-screen border-4 border-solid border-indigo-500"><Chatbox removePlots={removePlot} addPlot={addPlot} /></div>
    </div>

}