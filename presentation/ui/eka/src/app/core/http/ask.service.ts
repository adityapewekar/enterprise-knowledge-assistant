import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class AskService{
    private apiUrl:string = 'http://127.0.0.1:8000/';

    constructor(private http: HttpClient) {}

    sendMessage(message: string,role:string):Observable<any> {
        const headers = new HttpHeaders({'Content-Type': 'application/json','x-role': role});
        return this.http.post(this.apiUrl+"ask", { "query": message }, { headers });
    }

    updateKB(kbUpdate: string):Observable<any> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'X-Role': 'admin'
        });
        return this.http.post(`${this.apiUrl}/update-kb`, { kbUpdate }, { headers });
    }
}