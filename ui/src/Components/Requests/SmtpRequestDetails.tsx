import { Body1Strong, Divider, Textarea } from "@fluentui/react-components";
import {
    DssldrfRequest,
    SmtpRequest,
    SmtpResponse,
} from "../../Types/DssldrfRequest";

interface ISmtpRequestDetailsProps {
    details: DssldrfRequest;
}

export const SmtpRequestDetails = ({ details }: ISmtpRequestDetailsProps) => {
    // Assuming you have SmtpRequest and SmtpResponse types defined
    const req = details.request as SmtpRequest;
    const resp = details.response as SmtpResponse;

    return (
        <div className="stack vstack-gap">
            <div className="stack vstack">
                <Body1Strong>Mail From</Body1Strong>
                {req.mail_from}
            </div>

            <div className="stack vstack">
                <Body1Strong>Recipients</Body1Strong>
                {req.rcpt_tos.join(", ")}
            </div>

            <Divider style={{ paddingTop: 10, paddingBottom: 10 }} />

            <div className="stack vstack">
                <Body1Strong>Raw Data</Body1Strong>
                <Textarea readOnly={true} rows={10} value={req.data} />
            </div>

            <Divider style={{ paddingTop: 10, paddingBottom: 10 }} />

            <div className="stack vstack">
                <Body1Strong>Response</Body1Strong>
                {`${resp.code} ${resp.message}`}
            </div>
        </div>
    );
};
