import {
    Button,
    Text,
    Dialog,
    DialogActions,
    DialogBody,
    DialogContent,
    DialogSurface,
    DialogTitle,
    DialogTrigger,
    MessageBar,
    Select,
    makeStyles,
    ToolbarButton,
    Combobox,
    Option,
} from "@fluentui/react-components";
import { PeopleRegular } from "@fluentui/react-icons";
import { useEffect, useState } from "react";

import { AuthTable } from "./AuthTable";
import { DusseldorfAPI } from "../../DusseldorfApi";
import { Logger } from "../../Helpers/Logger";
import { User } from "../../Types/User";

export class PERMISSION {
    static READONLY = 0;
    static READWRITE = 10;
    static ASSIGNROLES = 20;
    static OWNER = 999;
}

const useStyles = makeStyles({
    dialog: {
        width: "500px",
    },
});

interface AuthDialogProps {
    zone: string;
}

export const AuthDialog = ({ zone }: AuthDialogProps) => {
    const styles = useStyles();

    const [users, setUsers] = useState<User[]>([]);
    const [username, setUsername] = useState<string>("");
    const [permission, setPermission] = useState<number>(PERMISSION.READONLY);
    const [error, setError] = useState<string>("");
    const [allSystemUsers, setAllSystemUsers] = useState<string[]>([]);

    const refreshUsers = () => {
        DusseldorfAPI.GetUsers(zone)
            .then((newUsers) => {
                setUsers(newUsers);
            })
            .catch((err) => {
                setUsers([]);
                Logger.Error(err);
            });
    };

    useEffect(() => {
        refreshUsers();
        // Fetch the list of all users so Admins can select them from the dropdown
        DusseldorfAPI.GetAllUsers()
            .then(setAllSystemUsers)
            .catch((err) =>
                Logger.Error("Failed to fetch system users: " + err),
            );
    }, [zone]);

    return (
        <Dialog>
            <DialogTrigger disableButtonEnhancement>
                <ToolbarButton icon={<PeopleRegular />}>Auth</ToolbarButton>
            </DialogTrigger>
            <DialogSurface className={styles.dialog}>
                <DialogBody>
                    <DialogTitle>Manage Users</DialogTitle>
                    <DialogContent className="stack vstack-gap">
                        <Text>
                            Add or remove users from this zone ({zone}). Please
                            select an existing user or type a new alias and
                            select a permission level.
                        </Text>
                        <AuthTable
                            users={users}
                            refreshUsers={refreshUsers}
                            zone={zone}
                        />
                        <div
                            className="stack hstack-gap"
                            style={{ paddingTop: "20px" }}
                        >
                            {/* Combobox replaces the Input field to allow both typing and selection */}
                            <Combobox
                                placeholder="Select or type user alias"
                                value={username}
                                onOptionSelect={(_, data) =>
                                    setUsername(data.optionValue || "")
                                }
                                onChange={(e) =>
                                    setUsername(e.currentTarget.value)
                                }
                                freeform
                                style={{ minWidth: "200px" }}
                            >
                                {allSystemUsers.map((user) => (
                                    <Option key={user} value={user}>
                                        {user}
                                    </Option>
                                ))}
                            </Combobox>

                            <Select
                                aria-label="Permission"
                                onChange={(_, data) => {
                                    setPermission(parseInt(data.value));
                                }}
                                value={permission}
                            >
                                <option value={PERMISSION.READONLY}>
                                    Read Only
                                </option>
                                <option value={PERMISSION.READWRITE}>
                                    Read Write
                                </option>
                                <option value={PERMISSION.ASSIGNROLES}>
                                    Assign Roles
                                </option>
                                <option value={PERMISSION.OWNER}>Owner</option>
                            </Select>

                            <Button
                                appearance="primary"
                                onClick={() => {
                                    if (username.length === 0) {
                                        setError("Please enter a user alias");
                                        return;
                                    }

                                    DusseldorfAPI.AddUserToZone(
                                        zone,
                                        username,
                                        permission,
                                    )
                                        .then(() => {
                                            setError("");
                                            setUsername("");
                                            refreshUsers();
                                        })
                                        .catch((err) => {
                                            setError(
                                                "An error occurred. User may already have access.",
                                            );
                                            Logger.Error(err);
                                        });
                                }}
                            >
                                Add User
                            </Button>
                        </div>
                        {error && (
                            <MessageBar intent="error">{error}</MessageBar>
                        )}
                    </DialogContent>
                    <DialogActions>
                        <DialogTrigger disableButtonEnhancement>
                            <Button>Close</Button>
                        </DialogTrigger>
                    </DialogActions>
                </DialogBody>
            </DialogSurface>
        </Dialog>
    );
};
