import {Component, Input, OnInit} from '@angular/core';
import {LogData} from '../model/logData';
import {HttpClient} from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import {RatingsModel} from '../model/ratings.model';
import {RatingsChartModel} from '../model/ratingsChart.model';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  lstLogs: LogData[];
  stockSymbol = 'AAPL';

  ratingsList: RatingsModel[];

  List: RatingsChartModel[];

  constructor(private httpClient: HttpClient) {
  }

  ngOnInit(): void {
  }

  getRequestLog(): void {
    this.httpClient
      .get('http://localhost:5000/requests/all')
      .pipe(map((response: any) => response))
      .subscribe(result => {
        this.lstLogs = result;
      });
  }

  getStockRating(): void{
    this.httpClient
      .get('http://localhost:5000/stock/ratings/NASDAQ/' + this.stockSymbol)
      .pipe(map((response: any) => response))
      .subscribe(result => {
        this.ratingsList = result;

        let i;

        for (i = 0; i < this.ratingsList.length; i++){
          this.List = this.aggregateRating(this.ratingsList[i]);
        }
      });
  }

  aggregateRating($ratingsModel): RatingsChartModel[] {

    let tempList: RatingsChartModel[] = [
      {value: 0, color: '#FF0000', size: '', legend: 'SELL'},
      {value: 0, color: '#F8C622', size: '', legend: 'HOLD'},
      {value: 0, color: '#008000', size: '', legend: 'BUY'},
    ];

    // Calculate the sums and group data (while tracking count)
    const reduced = $ratingsModel.analystsRatings.reduce( (m, d) => {
      if (!m[d.scaledRatings]){
        m[d.scaledRatings] = {rating: d.scaledRatings, count: 1};
        return m;
      }
      m[d.scaledRatings].count += 1;

      return m;
    }, {});

    for (const x in reduced) {
      if (x === 'BUY'){
        tempList[2].value = reduced[x].count;
      }
      if (x === 'HOLD'){
        tempList[1].value = reduced[x].count;
      }
      if (x === 'SELL'){
        tempList[0].value = reduced[x].count;
      }
    }

    tempList = this.calculateSize(tempList);
    return tempList;
  }

  calculateSize($tempList): RatingsChartModel[] {

    const tempList: RatingsChartModel[] = $tempList;

    let total = 0;
    const maxHeight = 160;

    tempList.forEach(element => {
      total += element.value;
    });

    tempList.forEach(element => {
      element.size = Math.round((element.value * maxHeight) / total) + '%';
    });
    return tempList;
  }

}
