import React, { useState } from 'react';
import { Project, columns } from './columns';
import { DataTable } from './table';
import { useParams } from 'react-router-dom'
import { axiosInstance } from '@/lib/utils';
import { AddProjectDialog } from './add_project';

export default function Projects() {
    const [projects, setProjects] = useState<Project[]>([]);
    const { user_id } = useParams()

    const getProjects = () => {
        // Fetch data from your API here.
        console.log("Getting projects");
        let url = `/projects/${user_id}`
        axiosInstance.get(url).then((response) => {
            let data = response.data;
            setProjects(data);
        })
    }

    React.useEffect(() => {
        getProjects();
    }, [user_id])
    return <div className="grid h-screen w-screen">
        <div>
            <h1 className='font-bold text-6xl'>Hello User!</h1>
            <p>Please select a project or create a new one</p>
            <AddProjectDialog user_id={user_id} getProjects={getProjects} />
            <hr style={{
                "border": "none",
                "borderTop": "3px double #333",
                "color": "#333",
                "overflow": "visible",
                "textAlign": "center",
                "height": "5px",
                "paddingBottom": '5px',
            }} />
            <br />
            <DataTable data={projects} columns={columns}></DataTable>
        </div>
    </div>
}

