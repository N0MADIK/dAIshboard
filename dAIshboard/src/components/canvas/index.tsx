import React from 'react';

import { Display } from './display';

function Canvas() {
    return <div className='h-screen overflow-hidden'>
        <div className="w-screen bg-blue-500 h-1/8">
            <h1 className="text-xl">Top Div</h1>
        </div>
        <div className="flex h-full w-screen">
            <div className="flex bg-green-500 w-1/12">
                <h2 className="text-lg">Left Div</h2>
            </div>
            <div className="flex w-11/12">
                <Display />
            </div>
        </div>
    </div>
}

export default Canvas