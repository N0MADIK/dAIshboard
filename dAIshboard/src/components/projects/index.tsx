import React from 'react';
import { Project, columns } from './columns';
import { DataTable } from './table';
import { useParams } from 'react-router-dom'

function getProjects(): Project[] {
    // Fetch data from your API here.
    return [
        {
            id: "728ed52f",
            name: "Test",
            owner: "Tester",
            created_on: "09-18-2024",
        },
        // ...
    ]
}

export default function Projects() {
    const data = getProjects();
    const { user_id } = useParams()

    React.useEffect(() => {
        console.log("HERE!! user id is", user_id)
    }, [user_id])
    return <div className="grid h-screen w-screen">
        <DataTable data={data} columns={columns}></DataTable>
    </div>
}

