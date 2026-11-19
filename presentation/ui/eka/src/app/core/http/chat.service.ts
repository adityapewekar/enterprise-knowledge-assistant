import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { API_CONFIG } from "../../environment";

@Injectable({
    providedIn: 'root'
})
export class ChatService{
    private apiUrl:string = `${API_CONFIG.BASE_URL}/`;

    constructor(private http: HttpClient) {}

    sendMessage(message: string, role: string):Observable<{ response?: string; error?: string }> {
        const headers = new HttpHeaders({'Content-Type': 'application/json','x-role': role});
        return this.http.post<{ response?: string; error?: string }>(
            this.apiUrl + "ask",
            { query: message },
            { headers }
        );
    }


    uploadDocument(file: File, roles: string[]): Observable<{ parsed_text: string; indexed: boolean }> {
        const formData = new FormData();
        formData.append('file', file);
        roles.forEach(role => formData.append('roles', role));
        return this.http.post<{ parsed_text: string; indexed: boolean }>(
            this.apiUrl + 'upload_doc',
            formData
        );
    }
}