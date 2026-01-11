import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { Logger } from "./Helpers/Logger";

const container = document.getElementById("woot");
if (!container) {
    Logger.Error("No root element found");
} else {
    const root = createRoot(container);
    root.render(
        <StrictMode>
            {" "}
            <App />{" "}
        </StrictMode>,
    );
}

Logger.Info("Dusseldorf.init()");
