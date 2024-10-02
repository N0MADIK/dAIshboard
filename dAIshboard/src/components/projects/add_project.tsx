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

interface AddProjectDialogProps {
    user_id: string,
    getProjects: () => void,
}

export function AddProjectDialog(props: AddProjectDialogProps) {
    const [open, setOpen] = useState(false);

    const [name, setName] = useState("");
    const [error, setError] = useState("");

    function onSubmit() {
        const data = {
            "name": name,
        }
        axiosInstance.post(`/projects/${props.user_id}/add`, data)
            .then((response) => {
                let data = response.data;
                if (data.success === true) {
                    props.getProjects();
                    setOpen(false);
                } else {
                    setError(data.error);
                }
            })

    }

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <Button className="bg-blue-500 text-white rounded hover:bg-blue-600 transition"
                >Add Project</Button>
            </DialogTrigger>
            <DialogContent className="bg-white">
                <DialogHeader>
                    <DialogTitle>Add New Project</DialogTitle>
                    <DialogDescription>
                        Fill out information to add a new project
                    </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="name" className="text-right">
                            Name
                        </Label>
                        <Input
                            id="name"
                            placeholder="Name"
                            className="col-span-3"
                            onChange={(event) => setName(event.target.value)}
                        />
                    </div>

                    {error != "" &&
                        <div className="grid grid-cols-4 items-center gap-4">
                            <Label htmlFor="error" className="text-right">
                                Error!
                            </Label>
                            <Label htmlFor="error" className="text-right">
                                {error}
                            </Label>
                        </div>
                    }
                </div>
                <DialogFooter>
                    <Button type="submit" onClick={onSubmit}>Add</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
