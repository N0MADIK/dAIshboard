
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { useState } from "react";

interface ChatBoxProps {
    removePlots: () => void
    addPlot: (query: string) => void
    error: string | null
}
export function Chatbox(props: ChatBoxProps) {
    const { removePlots, addPlot, error } = props;
    const [query, setQuery] = useState<string>("");

    const plotFromQuery = () => {
        console.log("Query:", query);
        addPlot(query);
        document.getElementById("queryBox").value = "";
        setQuery("");
    }

    const keyDownFnc = (event) => {
        if (event.which === 13) {
            if (!event.repeat) {
                plotFromQuery();
            }
        }
    }

    return <div className="w-screen">
        <Textarea id='queryBox' className="w-screen h-1/2" placeholder="Query goes here" onKeyDown={keyDownFnc} onChange={(e) => {
            setQuery(e.target.value);
        }} />
        <div className="flex gap-4">
            <Button onClick={removePlots}
            >Remove All Plots</Button>
            <br />
            <Button onClick={plotFromQuery}>
                Add New Plot
            </Button>
            {error && <h1>Error is: <b>{error}</b></h1>}
        </div>
    </div>
}