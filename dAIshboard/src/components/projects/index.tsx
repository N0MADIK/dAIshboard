import React from 'react';
import { Project, columns } from './columns';
import { DataTable } from './table';

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

    return <div className="grid h-screen w-screen">
        <DataTable data={data} columns={columns}></DataTable>
    </div>
}

