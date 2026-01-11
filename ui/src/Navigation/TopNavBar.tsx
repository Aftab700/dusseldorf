import {
    Avatar,
    Button,
    Dialog,
    DialogActions,
    DialogBody,
    DialogContent,
    DialogSurface,
    DialogTitle,
    DialogTrigger,
    Menu,
    MenuItem,
    MenuList,
    MenuPopover,
    MenuTrigger,
    Switch,
    Text,
} from "@fluentui/react-components";

import { Logo } from "../Components/Logo";
import {
    DismissRegular,
    SignOutRegular,
    WeatherMoonRegular,
    WeatherSunnyRegular,
} from "@fluentui/react-icons";
import { useState } from "react";
import { CacheHelper } from "../Helpers/CacheHelper";

interface ITopNavBarProps {
    apiError: boolean;
    darkTheme: boolean;
    toggleTheme: () => void;
    onLogout: () => void;
}

export const TopNavBar = ({
    darkTheme,
    toggleTheme,
    onLogout,
}: ITopNavBarProps) => {
    const [open, setOpen] = useState<boolean>(false);
    const userName = CacheHelper.GetUser();

    return (
        <>
            <div
                className="stack hstack-spread"
                style={{
                    height: "6%",
                    backgroundColor: "#003846",
                    paddingLeft: 10,
                    paddingRight: 10,
                }}
            >
                <Logo />
                <Menu>
                    <MenuTrigger disableButtonEnhancement>
                        <Button appearance="subtle">
                            <div
                                style={{
                                    display: "flex",
                                    flexDirection: "row",
                                    alignItems: "center",
                                }}
                            >
                                <Avatar name={userName} />
                                <Text
                                    style={{
                                        color: "#ffffff",
                                        paddingLeft: 10,
                                    }}
                                >
                                    {" "}
                                    {userName}
                                </Text>
                            </div>
                        </Button>
                    </MenuTrigger>
                    <MenuPopover>
                        <MenuList>
                            <MenuItem onClick={toggleTheme} persistOnClick>
                                <div
                                    style={{
                                        display: "flex",
                                        flexDirection: "row",
                                        alignItems: "center",
                                    }}
                                >
                                    {darkTheme ? (
                                        <WeatherMoonRegular fontSize={20} />
                                    ) : (
                                        <WeatherSunnyRegular fontSize={20} />
                                    )}
                                    <Switch
                                        checked={darkTheme}
                                        label={
                                            darkTheme
                                                ? "Use light theme"
                                                : "Use dark theme"
                                        }
                                        labelPosition="before"
                                    />
                                </div>
                            </MenuItem>
                            <MenuItem
                                icon={<SignOutRegular fontSize={20} />}
                                onClick={() => setOpen(true)}
                            >
                                Sign out
                            </MenuItem>
                        </MenuList>
                    </MenuPopover>
                </Menu>
            </div>

            <Dialog open={open} onOpenChange={(_, data) => setOpen(data.open)}>
                <DialogSurface>
                    <DialogBody>
                        <DialogTitle>Sign Out</DialogTitle>
                        <DialogContent>
                            Do you want to sign out and clear the session?
                        </DialogContent>
                        <DialogActions>
                            <Button
                                appearance="primary"
                                icon={<SignOutRegular />}
                                onClick={() => {
                                    setOpen(false);
                                    onLogout();
                                }}
                            >
                                Sign out
                            </Button>
                            <DialogTrigger disableButtonEnhancement>
                                <Button
                                    appearance="secondary"
                                    icon={<DismissRegular />}
                                >
                                    Cancel
                                </Button>
                            </DialogTrigger>
                        </DialogActions>
                    </DialogBody>
                </DialogSurface>
            </Dialog>
        </>
    );
};
