
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { useState } from "react";

interface ChatBoxProps {
    removePlots: () => void
    addPlot: () => void
}
export function Chatbox(props: ChatBoxProps) {
    const { removePlots, addPlot } = props;
    const [query, setQuery] = useState<string>("");

    const TestAddPlot = () => {
        console.log("Query:", query);
    }

    return <div className="w-screen">
        <Textarea className="w-11/12 h-1/2" placeholder="Query goes here" onChange={(e) => {
            setQuery(e.target.value);
        }} />
        <div className="flex flex-row-2">
            <Button onClick={removePlots}
            >Remove All Plots</Button>
            <br />
            <Button onClick={TestAddPlot}>
                Add New Plot
            </Button>
        </div>
    </div>
}