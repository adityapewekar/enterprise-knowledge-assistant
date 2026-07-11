import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class ChatService{
    private apiUrl:string = 'http://127.0.0.1:8000/';

    constructor(private http: HttpClient) {}

    sendMessage(message: string,role:string):Observable<any> {
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