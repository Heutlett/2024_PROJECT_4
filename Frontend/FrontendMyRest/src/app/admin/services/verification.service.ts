import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VerificationService {

  constructor(private http:HttpClient) { }

  getReservaciones():Observable<any>{
    const url = 'http://192.168.49.2:30014/obtener-reserva/';
    return this.http.get<any>(url);
  }

  getReservacionesPasadas(client1:string):Observable<any>{
    const url = `http://192.168.49.2:30017/obtener-reserva/?time=futuras&token=${client1}`;
    return this.http.get<any>(url);
  }

  getReservacionesFuturas(client1:string):Observable<any>{
    // http://192.168.49.2::30015/obtener-reserva/?time=pasadas&token=
    const url = `http://192.168.49.2:30015/obtener-reserva/?time=pasadas&token=${client1}`;
    return this.http.get<any>(url);
  }
}
