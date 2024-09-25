
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { useState } from "react";

interface ChatBoxProps {
    removePlots: () => void
    addPlot: (query: string) => void
}
export function Chatbox(props: ChatBoxProps) {
    const { removePlots, addPlot } = props;
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
        <Textarea id='queryBox' className="w-11/12 h-1/2" placeholder="Query goes here" onKeyDown={keyDownFnc} onChange={(e) => {
            setQuery(e.target.value);
        }} />
        <div className="flex flex-row-2">
            <Button onClick={removePlots}
            >Remove All Plots</Button>
            <br />
            <Button onClick={plotFromQuery}>
                Add New Plot
            </Button>
        </div>
    </div>
}