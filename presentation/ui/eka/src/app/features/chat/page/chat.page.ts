import { Component,signal  } from '@angular/core';
import { AskService } from '../../../core/http/ask.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-chat',
  imports: [FormsModule,CommonModule],
  templateUrl: './chat.page.html',
  styleUrl: './chat.page.css',
})
export class ChatPage {
  messages=signal<{role:string,content:string}[]>([]);
  userInput="";
  KbUpdate="";
  selectedRole:string="employee";

  constructor(private askService: AskService) {}

  sendMessage() {
    const userMessage = this.userInput.trim();
    if (!userMessage) return;
    
    this.messages.update(msg => [...msg, { role: 'user', content: userMessage }]);

    this.askService.sendMessage(userMessage,this.selectedRole).subscribe(res=>{
      this.messages.update(msg => [...msg, { role: 'assistant', content: res.response }]);
    });

    this.userInput = '';
  }

  updateKB(){
    const kbText= this.KbUpdate.trim();
    if(!kbText) return;
    
    this.askService.updateKB(kbText).subscribe(res=>{
      this.KbUpdate = '';
    });
  }
}

