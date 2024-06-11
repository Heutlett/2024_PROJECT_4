import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MenuService {

  constructor(private http:HttpClient) { }

  getMenus():Observable<any>{
    return this.http.get<any>('http://192.168.49.2:30019/obtener-menu');
  }

  getRecomendacion(entry:string):Observable<any>{
    return this.http.get<any>(`http://192.168.49.2:30020/obtener-recomendacion?${entry}`);
  }
}
