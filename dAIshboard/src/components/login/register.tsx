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


export function RegisterDialog() {
    const [open, setOpen] = useState(false);

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    function onSubmit() {
        const data = {
            "name": name,
            "email": email,
            "password": password,
        }
        axiosInstance.post(`/register`, data)
            .then((response) => {
                let data = response.data;
                if (data.success === true) {
                    setOpen(false);
                } else {
                    setError(data.error);
                }
            })

    }

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <Button className="w-full bg-blue-500 text-white rounded hover:bg-blue-600 transition"
                >Register</Button>
            </DialogTrigger>
            <DialogContent className="bg-white">
                <DialogHeader>
                    <DialogTitle>Register User</DialogTitle>
                    <DialogDescription>
                        Fill out information to register a user
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

                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="email" className="text-right">
                            Email
                        </Label>
                        <Input
                            id="email"
                            placeholder="Email"
                            className="col-span-3"
                            onChange={(event) => setEmail(event.target.value)}
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="password" className="text-right">
                            Password
                        </Label>
                        <Input
                            type="password"
                            id="password"
                            placeholder="Password"
                            className="col-span-3"
                            onChange={(event) => setPassword(event.target.value)}
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
                    <Button type="submit" onClick={onSubmit}>Register</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
