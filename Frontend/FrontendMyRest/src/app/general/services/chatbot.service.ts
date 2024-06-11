import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

  constructor(private http:HttpClient) {
  }

  chatMessage(message: string) {
    return this.http.get<any>(`http://192.168.49.2:30022/feedback-chatbot?texto=${message}`);
  }
}
