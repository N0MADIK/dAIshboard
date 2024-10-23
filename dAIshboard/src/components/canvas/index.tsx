
import { Display } from './display';
import { TopNav } from './top_nav/page';

function Canvas() {
    return <div className='h-screen overflow-hidden'>
        <div className="w-screen bg-blue-500 h-1/8 flex flex-col-1">
            <TopNav />
        </div>
        <div className="flex h-full w-screen">
            <div className="flex w-10/12">
                <Display />
            </div>
        </div>
    </div>
}

export default Canvas