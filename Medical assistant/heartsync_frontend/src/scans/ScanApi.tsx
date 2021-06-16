import axios from "axios";
import {authConfig, config, withLogs} from "../shared";
import {ScanProps} from "./ScanProps";
export const baseUrl = 'localhost:5000';
const scansUrl = `http://${baseUrl}/api/scans/`;

export interface AuthProps {
    accessToken: string;
    tokenType: string;
    message: string;
}

export const uploadConfig = (token?: string) => ({
    headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${token}`,
    },
});

export const getScans: (token?: string) => Promise<ScanProps[]> = (token) => {
    var getScansUrl = scansUrl + 'get'
    return withLogs(axios.get(getScansUrl, authConfig(token)), 'getScans');
}

export const getScanApi: (token: string, scanid: string) => Promise<ScanProps[]> = (token, scanid) => {
    var getScanUrl = scansUrl + 'getone/' + `${scanid}`;
    return withLogs(axios.get(getScanUrl, authConfig(token)), 'getScan');
}

export const uploadScan: (token: string, file: FormData) => Promise<ScanProps> = (token, file) => {
    var uploadUrl = scansUrl + 'add';
    return withLogs(axios.post(uploadUrl, file, uploadConfig(token)), "uploadScan");
}
