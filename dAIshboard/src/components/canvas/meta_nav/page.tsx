
import { useEffect, useState } from 'react';
import FileExplorer, { FileItem } from './explorer';
import { axiosInstance } from '@/lib/utils';
import { useParams } from 'react-router-dom'


const sampleData = [
    {
        name: 'data',
        type: 'folder',
        children: [
            {
                name: 'Stock', type: 'folder', children: [
                    { "name": "type", type: "folder", children: [{ "name": "xlsx", type: "file" }] },
                    {
                        "name": "columns", type: 'folder', children: [
                            {
                                "name": "Date", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "datetime64[ns]", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "Open", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "float64", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "High", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "float64", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "Low", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "float64", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "Close", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "float64", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "Adj Close", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "float64", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "Volume", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "int64", "type": "file" }] }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                name: 'Stock 2', type: 'folder', children: [
                    { "name": "type", type: "folder", children: [{ "name": "xlsx", type: "file" }] },
                    {
                        "name": "columns", type: 'folder', children: [
                            {
                                "name": "Date", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "datetime64[ns]", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "Open", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "float64", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "High", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "float64", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "Low", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "float64", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "Close", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "float64", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "Adj Close", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "float64", "type": "file" }] }
                                ]
                            },
                            {
                                "name": "Volume", type: 'folder', children: [
                                    { "name": "type", type: 'folder', children: [{ "name": "int64", "type": "file" }] }
                                ]
                            }
                        ]
                    }
                ]
            },
        ],
    }
];



export function MetaNav() {

    const [projectMeta, setProjectMeta] = useState<FileItem[]>([]);
    const { user_id, project_id } = useParams()

    useEffect(() => {
        let url = `/projects/${user_id}/${project_id}/metadata`
        console.log("URL IS ", url);
        let Metadata: FileItem[] = []
        axiosInstance.get(url).then((response) => {
            let response_data = response.data;
            let dataBlock = {
                name: 'data',
                type: 'folder',
                children: response_data.data
            }
            console.log(dataBlock);
            Metadata.push(dataBlock as FileItem);
            setProjectMeta(Metadata);
        })
    }, [])
    return <FileExplorer items={projectMeta} />
}