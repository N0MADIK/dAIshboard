
import { useEffect, useState } from 'react';
import FileExplorer, { FileItem } from './explorer';
import { axiosInstance } from '@/lib/utils';
import { useParams } from 'react-router-dom'
import { UploadFileDialog } from './uploadFile';

export function MetaNav() {

    const [projectMeta, setProjectMeta] = useState<FileItem[]>([]);
    const { user_id, project_id } = useParams()

    useEffect(() => {
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
    }, [])
    return <div>
        <UploadFileDialog />

        <FileExplorer items={projectMeta} />
    </div>
}