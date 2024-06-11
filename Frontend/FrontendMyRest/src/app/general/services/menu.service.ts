import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MenuService {

  constructor(private http:HttpClient) { }

  getMenus():Observable<any>{
    return this.http.get<any>('https://us-central1-soa-project3.cloudfunctions.net/obtener-menu');
  }

  getRecomendacion(entry:string):Observable<any>{
    return this.http.get<any>(`https://us-central1-soa-project3.cloudfunctions.net/obtener-recomendacion/?${entry}`);
  }
}
