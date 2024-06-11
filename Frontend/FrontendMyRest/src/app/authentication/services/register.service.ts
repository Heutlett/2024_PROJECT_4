import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { Injectable } from '@angular/core';
import {catchError} from 'rxjs/operators'; 


@Injectable({
  providedIn: 'root'
})
export class RegisterService {
  constructor(private http:HttpClient) { }

  createUser(registerInfo:any):Observable<any>{
    const url = "http://192.168.49.2:30018/crear-usuario"
    
    

    return this.http.post<any>(url, registerInfo).pipe(
      catchError(this.handleError)
    );
    //return this.http.post<any>(url, registerInfo).pipe(catchError(this.handleError));
  }

  changePassword(passInfo:any){
    const url = "http://192.168.49.2:30007/cambiar-contrasena"
    return this.http.post<any>(url, passInfo).pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    // Return an observable with a user-facing error message.
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }
  
}


