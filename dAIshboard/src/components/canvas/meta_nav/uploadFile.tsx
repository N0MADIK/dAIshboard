import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useState } from "react";
import { axiosInstance } from "@/lib/utils";
import { useParams } from 'react-router-dom'

interface UploadFileDialogProps {
    getProjectDataMetaData: () => void
}

export function UploadFileDialog(props: UploadFileDialogProps) {
    const [open, setOpen] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const { user_id, project_id } = useParams()

    const handleUpload = async () => {
        if (!file) {
            setError('Please select a file to upload.');
            return;
        }

        setUploading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axiosInstance.post(`/upload/data/${user_id}/${project_id}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            let data = response.data;
            if (data.success === true) {
                setError(`File uploaded successfully`);
                props.getProjectDataMetaData();
                setOpen(false);
            } else {
                setError(`File upload failed: ${data.error}`);
            }
        } catch (error) {
            setError(`Error uploading file: ${error}`);
        } finally {
            setUploading(false);
        }
    };


    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setFile(event.target.files[0]);
        }
    };

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <Button className="w-full bg-blue-500 text-white rounded hover:bg-blue-600 transition"
                >Upload</Button>
            </DialogTrigger>
            <DialogContent className="bg-white">
                <DialogHeader>
                    <DialogTitle>Upload New Data</DialogTitle>
                    <DialogDescription>
                        Select a file to upload new data
                    </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Input
                            id="file"
                            placeholder="File"
                            className="col-span-3"
                            type="file"
                            onChange={handleFileChange}
                        />
                    </div>

                    {error != null &&
                        <div className="grid grid-cols-4 items-center gap-4">
                            <Label htmlFor="error" className="text-right">
                                Message:
                            </Label>
                            <Label htmlFor="error" className="text-right">
                                {error}
                            </Label>
                        </div>
                    }
                </div>
                <DialogFooter>
                    <Button onClick={handleUpload} disabled={uploading}>
                        {uploading ? 'Uploading...' : 'Upload'}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
