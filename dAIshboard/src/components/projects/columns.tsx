import { ColumnDef } from "@tanstack/react-table"

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Project = {
    id: string
    name: string
    owner: string
    created_on: string
}

export const columns: ColumnDef<Project>[] = [
    {
        accessorKey: "id",
        header: "id",
        meta: {
            type: 'string'
        }
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
