import React from 'react';

import { Display } from './display';
import { MetaNav } from './meta_nav/page';
import { TopNav } from './top_nav/page';

function Canvas() {
    return <div className='h-screen overflow-hidden'>
        <div className="w-screen bg-blue-500 h-1/8">
            <h1 className="text-xl"><TopNav /></h1>
        </div>
        <div className="flex h-full w-screen">
            <div className="flex bg-green-500 w-2/12">
                <h2 className="text-lg"><MetaNav /></h2>
            </div>
            <div className="flex w-10/12">
                <Display />
            </div>
        </div>
    </div>
}

export default Canvas