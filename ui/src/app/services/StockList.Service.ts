import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import {Observable} from 'rxjs';


@Injectable()
export class StockListService {
  constructor(private http: HttpClient) {
  }

  getStockList(): Observable<any> {
    const headers = new HttpHeaders();
    headers.set('Content-Type', 'application/json');

    return this.http.get('http://localhost:5000/stock/all', { headers });
  }
}
