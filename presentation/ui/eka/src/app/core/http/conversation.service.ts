import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { API_CONFIG } from "../../environment";
import { Observable } from "rxjs";

export interface ConversationMessage {
    role: 'user' | 'assistant';
    content: string;
}


@Injectable({ providedIn: 'root' })
export class ConversationService{  
    
        private apiUrl:string = `${API_CONFIG.BASE_URL}/`;
    
        constructor(private http: HttpClient) {}
    
    
    getConversation(): Observable<{ messages: ConversationMessage[] }> {
        return this.http.get<{ messages: ConversationMessage[] }>(
            `${this.apiUrl}conversations/me/messages`
        );
    }

    clearConversation(): Observable<{ cleared: boolean }> {
        return this.http.delete<{ cleared: boolean }>(
            `${this.apiUrl}conversations/me/messages`
        );
    }
}