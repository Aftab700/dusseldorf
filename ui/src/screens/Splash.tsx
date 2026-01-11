import {
    Button,
    Caption1,
    Input,
    Link,
    Select,
    Text,
    Title3,
} from "@fluentui/react-components";
import { LockClosedRegular } from "@fluentui/react-icons";
import { useState } from "react";
import { DusseldorfAPI } from "../DusseldorfApi";
import { Logger } from "../Helpers/Logger";

import "../Styles/Stack.css";

interface ISplashProps {
    onLoginSuccess: () => void;
}

export const Splash = ({ onLoginSuccess }: ISplashProps) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            await DusseldorfAPI.Login(username, password);
            onLoginSuccess();
        } catch (err: any) {
            setError(err.message || "Authentication failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            className="stack vstack-gap"
            style={{ padding: 100, maxWidth: 400 }}
        >
            <Title3>Project Dusseldorf</Title3>

            <form className="stack vstack-gap" onSubmit={handleLogin}>
                <Input
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <Input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                {error && <Text style={{ color: "red" }}>{error}</Text>}

                <Button
                    appearance="primary"
                    icon={<LockClosedRegular />}
                    type="submit"
                    disabled={loading}
                >
                    {loading ? "Signing in..." : "Sign in"}
                </Button>
            </form>

            <Caption1>
                <Link inline href="https://github.com/microsoft/dusseldorf">
                    Documentation
                </Link>
            </Caption1>
        </div>
    );
};
