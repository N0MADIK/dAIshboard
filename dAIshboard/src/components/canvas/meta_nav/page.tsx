
import { useEffect, useState } from 'react';
import FileExplorer, { FileItem } from './explorer';
import { axiosInstance } from '@/lib/utils';
import { useParams } from 'react-router-dom'
import { UploadFileDialog } from './uploadFile';
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"
import { Button } from "@/components/ui/button"

export function MetaNav() {

    const [projectMeta, setProjectMeta] = useState<FileItem[]>([]);
    const { user_id, project_id } = useParams()

    const getProjectDataMetaData = () => {
        let url = `/projects/${user_id}/${project_id}/metadata`
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
    }
    useEffect(() => {
        getProjectDataMetaData();
    }, [])
    return <div>
        <Popover>
            <PopoverTrigger asChild>
                <Button>Menu</Button>
            </PopoverTrigger>
            <PopoverContent className="w-80 bg-blue-500">
                <UploadFileDialog getProjectDataMetaData={getProjectDataMetaData} />
                <FileExplorer items={projectMeta} />
            </PopoverContent>
        </Popover>
    </div>
}