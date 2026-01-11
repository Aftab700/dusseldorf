import {
    FluentProvider,
    Spinner,
    webDarkTheme,
    webLightTheme,
} from "@fluentui/react-components";
import { createContext, useEffect, useState } from "react";
import { HashRouter } from "react-router-dom";

import { DusseldorfAPI } from "./DusseldorfApi";
import { CacheHelper } from "./Helpers/CacheHelper";
import { Logger } from "./Helpers/Logger";
import { ThemeHelper } from "./Helpers/ThemeHelper";
import { LeftNav } from "./Navigation/LeftNav";
import { TopNavBar } from "./Navigation/TopNavBar";
import { ScreenRouter } from "./screens/ScreenRouter";
import { Splash } from "./screens/Splash";

import "./App.css";
import "./Styles/Stack.css";

export const DomainsContext = createContext<string[]>([]);

export const App = () => {
    const [darkTheme, setDarkTheme] = useState<boolean>(
        ThemeHelper.Get() === "dark",
    );
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(
        !!CacheHelper.GetToken(),
    );
    const [domains, setDomains] = useState<string[]>();

    useEffect(() => {
        if (isAuthenticated && !domains) {
            DusseldorfAPI.GetDomains()
                .then((newDomains) => {
                    setDomains(newDomains.length > 0 ? newDomains : undefined);
                })
                .catch((err) => {
                    Logger.Error(err);
                    if (err.message.includes("401")) handleLogout();
                });
        }
    }, [isAuthenticated]);

    const handleLogout = () => {
        CacheHelper.Clear();
        setIsAuthenticated(false);
        setDomains(undefined);
    };

    return (
        <FluentProvider theme={darkTheme ? webDarkTheme : webLightTheme}>
            {!isAuthenticated ? (
                <Splash onLoginSuccess={() => setIsAuthenticated(true)} />
            ) : (
                <>
                    {domains ? (
                        <DomainsContext.Provider value={domains}>
                            <HashRouter basename="/">
                                <div
                                    style={{ height: "100vh", width: "100vw" }}
                                >
                                    <TopNavBar
                                        apiError={false}
                                        darkTheme={darkTheme}
                                        toggleTheme={() => {
                                            setDarkTheme(!darkTheme);
                                            ThemeHelper.Set(
                                                darkTheme ? "light" : "dark",
                                            );
                                        }}
                                        onLogout={handleLogout}
                                    />
                                    <div
                                        className="stack hstack"
                                        style={{ width: "100%", height: "94%" }}
                                    >
                                        <LeftNav refreshToken={() => {}} />
                                        <ScreenRouter />
                                    </div>
                                </div>
                            </HashRouter>
                        </DomainsContext.Provider>
                    ) : (
                        <Spinner size="large" label="Loading data from API" />
                    )}
                </>
            )}
        </FluentProvider>
    );
};
