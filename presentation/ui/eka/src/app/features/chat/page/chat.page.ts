import { Component,signal  } from '@angular/core';
import { ChatService } from '../../../core/http/chat.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-chat',
  imports: [
    FormsModule,
    CommonModule,
    MatFormFieldModule,
    MatSelectModule,
    MatOptionModule,
    MatInputModule,
    MatButtonModule  
  ],
  templateUrl: './chat.page.html',
  styleUrl: './chat.page.css',
})
export class ChatPage {
  messages=signal<{role:string,content:string}[]>([]);
  userInput="";
  KbUpdate="";
  selectedRole:string="employee";
  selectedRoleKB:string[]=[];
  roles: string[] = ['employee', 'admin'];


  constructor(private askService: ChatService) {}

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
    
    this.askService.updateKB(kbText,this.selectedRoleKB).subscribe(res=>{
      this.KbUpdate = '';
    });
  }
}

