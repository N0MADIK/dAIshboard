import React from 'react';
import { Rnd } from 'react-rnd';
import Plot from 'react-plotly.js';

export interface PlotData {
    id: string,
    width: number,
    height: number,
    x: number,
    y: number,
    data: any[],
    layout: any,
    frames: any[],
    config: any,
    index: number,
    ts: number
}

export interface PlotProps {
    state: PlotData,
    removePlotAt: (data: PlotData) => void
}




class PlotArea extends React.Component<PlotData> {
    constructor(props: any) {
        super(props);
        this.state = props.state;
    }



    render() {
        return <Rnd
            size={{ width: this.state.width, height: this.state.height }}
            position={{ x: this.state.x, y: this.state.y }}
            onDragStop={(e, d) => { console.log("HERE", e, d); this.setState({ x: d.x, y: d.y }) }}
            onResize={(e, direction, ref, delta, position) => {
                const newLayout = { ...this.state.layout, height: ref.offsetHeight, width: ref.offsetWidth };
                this.setState({
                    width: ref.offsetWidth,
                    height: ref.offsetHeight,
                    layout: newLayout,
                });
            }}
            bounds=".showArea"
            dragHandleClassName="handle"
        >
            <div className=''>
                <div className='flex bg-gray-50'>
                    <div className='handle flex items-center justify-center w-11/12'>
                        <h1>{this.state.id}</h1>
                    </div>
                    <div className='flex items-center justify-center w-1/12 w-fit text-red-900 font-bold'>
                        <button
                            onClick={
                                (e) => {
                                    this.props.removePlotAt(this.state);
                                }
                            }
                        >X</button>
                    </div>
                </div>
                <Plot
                    data={this.state.data}
                    layout={this.state.layout}
                />
            </div>
        </Rnd>
    }
}

export default PlotArea;