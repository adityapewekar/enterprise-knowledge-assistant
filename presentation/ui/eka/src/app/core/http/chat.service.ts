import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { API_CONFIG } from "../../environment";

@Injectable({
    providedIn: 'root'
})
export class ChatService{
    private apiUrl:string = API_CONFIG.BASE_URL;

    constructor(private http: HttpClient) {}

    sendMessage(message: string, role: string):Observable<any> {
        const headers = new HttpHeaders({'Content-Type': 'application/json','x-role': role});
        return this.http.post(this.apiUrl+"ask", { "query": message }, { headers });
    }

    updateKB(kbUpdate: string, roles: string[]):Observable<any> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        return this.http.post(this.apiUrl+"update_kb_article", { article: kbUpdate, roles }, { headers });
    }
}