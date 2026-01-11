export class Logger {
    // No-op for compatibility with existing calls
    static init = () => {};

    static RESET = "\u001b[0m";
    static RED = "\u001b[1;31m";
    static GREEN = "\u001b[1;32m";
    static YELLOW = "\u001b[1;33m";

    static Info = (msg: string) => {
        console.log(this.GREEN + "[INFO] " + msg + this.RESET);
    };

    static Warn = (msg: string) => {
        console.warn(this.YELLOW + "[WARN] " + msg + this.RESET);
    };

    static Error = (msg: any) => {
        const msgStr = String(msg);
        console.error(this.RED + "[ERROR] " + msgStr + this.RESET);
    };

    static Exception = (ex: any) => {
        console.error("[EXCEPTION]", ex);
    };

    static PageView = (path: string) => {
        console.log(`[PAGE VIEW] ${path}`);
    };

    static Trace = (msg: string, level: string) => {
        console.log(`[TRACE - ${level}] ${msg}`);
    };
}
