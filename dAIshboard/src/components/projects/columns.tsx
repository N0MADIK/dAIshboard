import { ColumnDef } from "@tanstack/react-table"
import { UserContext } from "@/lib/utils";
import { useContext } from 'react';

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Project = {
    id: string
    name: string
    owner: string
    created_on: string
}

interface IDCellProps {
    project_id: string
}

function IDCell(props: IDCellProps) {
    const { user_data } = useContext(UserContext);
    const url = `/canvas/${user_data.id}/${props.project_id}`
    return <a href={url}>{props.project_id}</a>
}

export const columns: ColumnDef<Project>[] = [
    {
        accessorKey: "id",
        header: "id",
        meta: {
            type: 'string'
        },
        cell: ({ row }) => (<IDCell project_id={row.getValue("id")} />)
    },
    {
        accessorKey: "name",
        header: "name",
        meta: {
            type: 'string'
        }
    },
    {
        accessorKey: "owner",
        header: "owner",
        meta: {
            type: 'string'
        }
    },
    {
        accessorKey: "created_on",
        header: "created_on",
        meta: {
            type: 'date'
        }
    },
]
