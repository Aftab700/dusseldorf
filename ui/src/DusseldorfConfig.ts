const API_HOST =
    process.env.REACT_APP_API_HOST ??
    window.localStorage.getItem("api_host") ??
    "/api";

export default {
    domain: "",
    public_zone: "public",
    loaded: false,
    api_host: API_HOST,
};
