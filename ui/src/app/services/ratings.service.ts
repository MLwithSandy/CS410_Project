import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';

@Injectable()
export class RatingsService
{
  constructor(private httpClient: HttpClient) { }

  getRatings(): Observable<any>{
    return this.httpClient.get('http://localhost:5000/requests/all');
  }
}
