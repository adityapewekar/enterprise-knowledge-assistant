import { Component, OnInit, signal } from '@angular/core';
import { ChatService } from '../../../core/http/chat.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ConversationMessage, ConversationService } from '../../../core/http/conversation.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-chat',
  imports: [
    FormsModule,
    CommonModule,
    MatFormFieldModule,
    MatSelectModule,
    MatOptionModule,
    MatInputModule,
    MatButtonModule,
    MatSnackBarModule
  ],
  templateUrl: './chat.page.html',
  styleUrl: './chat.page.css',
})
export class ChatPage implements OnInit {
  messages = signal<ConversationMessage[]>([]);
  userInput="";
  selectedRole:string="employee";
  selectedRoleKB:string[]=[];
  selectedDocument: File | null = null;
  roles: string[] = ['employee', 'admin'];
  isSending = false;
  isUploading = false;
  isLoadingHistory = true;
  historyError = '';
  requestError = '';


  constructor(private askService: ChatService,
                      private conversationService: ConversationService,
                      private snackBar: MatSnackBar
  ) {}

  ngOnInit() {
    this.conversationService.getConversation().subscribe({
      next: result => {
        this.messages.set(result.messages);
        this.isLoadingHistory = false;
      },
      error: () => {
        this.historyError = 'Conversation history could not be loaded. Please refresh to try again.';
        this.isLoadingHistory = false;
      }
    });
  }

  sendMessage() {
    const userMessage = this.userInput.trim();
    if (!userMessage || this.isSending || this.isLoadingHistory || this.historyError) return;
    
    this.messages.update(msg => [...msg, { role: 'user', content: userMessage }]);
    this.isSending = true;
    this.requestError = '';

    this.askService.sendMessage(userMessage, this.selectedRole).subscribe({
      next: res => {
        if (res.error) {
          this.messages.update(msg => msg.slice(0, -1));
          this.requestError = res.error;
        } else {
          const answer = res.response || 'The assistant returned no response.';
          this.messages.update(msg => [...msg, { role: 'assistant', content: answer }]);
        }
        this.isSending = false;
      },
      error: () => {
        this.messages.update(msg => msg.slice(0, -1));
        this.requestError = 'Your message could not be saved or answered. Please try again.';
        this.isSending = false;
      }
    });

    this.userInput = '';
  }

  clearHistory() {
    if (this.isSending || this.isLoadingHistory || !this.messages().length) return;
    this.conversationService.clearConversation().subscribe({
      next: () => {
        this.messages.set([]);
        this.requestError = '';
        this.historyError = '';
      },
      error: () => {
        this.requestError = 'Conversation history could not be cleared. Please try again.';
      }
    });
  }

  onDocumentSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    this.selectedDocument = input.files?.[0] ?? null;
    this.requestError = '';
  }

  uploadDocument() {
    if (!this.selectedDocument || !this.selectedRoleKB.length || this.isUploading) return;

    const file = this.selectedDocument;
    this.isUploading = true;
    this.requestError = '';

    this.askService.uploadDocument(file, this.selectedRoleKB).subscribe({
      next: result => {
        const message = result.indexed
          ? `${file.name} uploaded and indexed successfully.`
          : `${file.name} uploaded, but no text was available to index.`;
        this.showUploadNotification(message);
        this.selectedDocument = null;
        this.isUploading = false;
      },
      error: (error: HttpErrorResponse) => {
        this.showUploadNotification(
          error.error?.detail || 'The document could not be uploaded. Please try again.',
          true
        );
        this.isUploading = false;
      }
    });
  }

  private showUploadNotification(message: string, isError = false) {
    this.snackBar.open(message, 'Dismiss', {
      duration: 5000,
      horizontalPosition: 'end',
      verticalPosition: 'top',
      politeness: isError ? 'assertive' : 'polite',
      panelClass: isError ? 'upload-toast-error' : 'upload-toast-success'
    });
  }
}
