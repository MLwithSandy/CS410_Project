import {AfterViewInit, Component, Input, OnInit, ViewChild} from '@angular/core';
import {LogData} from '../model/logData';
import {HttpClient} from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import {RatingsModel} from '../model/ratings.model';
import {RatingsChartModel} from '../model/ratingsChart.model';
import {AnalystsRating} from '../model/analystsRating';
import {MatTableDataSource} from '@angular/material/table';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';
import {FormControl} from '@angular/forms';
import {RatingsCardModel} from '../model/ratings-card.model';
import {Constants} from '../model/Constants.model';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, AfterViewInit {

  lstLogs: LogData[];

  @Input()
  stockSymbol = 'AAPL';

  // ratingsList: RatingsModel[];

  ratingsList: RatingsModel;
  ratingsCardModel: RatingsCardModel;

  List: RatingsChartModel[];

  dataSource = new MatTableDataSource();
  @ViewChild(MatPaginator, { static: false }) paginator: MatPaginator;
  @ViewChild(MatSort, { static: false }) sort: MatSort;

  // displayedColumns = ['ratingDate', 'stockSymbol', 'ratingAgency', 'ratingAssigned'];
  displayedColumns = ['ratingDate', 'ratingAgency', 'ratingAssigned'];

  constructor(private httpClient: HttpClient) {
  }

  ngOnInit(): void {
    this.ratingsCardModel = new RatingsCardModel();
    this.ratingsList = new RatingsModel();
    this.ratingsList.analystsRatings = [];

  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  getRequestLog(): void {
    this.httpClient
      .get('http://localhost:5000/requests/all')
      .pipe(map((response: any) => response))
      .subscribe(result => {
        this.lstLogs = result;
      });
  }

 getSearchResult(): void{
    this.getStockRating().subscribe(
      result => {
        this.ratingsList = result[0];
        this.getRatingsCardStyle();
        this.getRatingForChart();
        this.prepareRatingDataTable();
      }
    );

  }

  getRatingForChart(): void{
    this.List = this.aggregatedRatingForChart(this.ratingsList);
  }

  prepareRatingDataTable(): void{
    this.dataSource.data = [];

    this.dataSource.data = this.ratingsList.analystsRatings;

    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
    console.log(this.dataSource.data);
  }

  getRatingsCardStyle(): void{
      this.ratingsCardModel.imgPath = '/assets/images/' + this.ratingsList.overallRating + '.svg';
      this.ratingsCardModel.btnBgColor =
        (this.ratingsList.overallRating === 'BUY' ? Constants.COLOR[0]
          : this.ratingsList.overallRating === 'HOLD' ? Constants.COLOR[1]
          : Constants.COLOR[2]);

  }


  getStockRating(): any{

    // this.ratingsList = [];

    console.log('stockSymbol: ' + this.stockSymbol  );
    return this.httpClient
      .get('http://localhost:5000/stock/ratings/NASDAQ/' + this.stockSymbol)
      .pipe(map((response: any) =>  response));

  }

  getSentiment(): any{

    // this.ratingsList = [];

    console.log('stockSymbol: ' + this.stockSymbol  );
    return this.httpClient
      .get('http://localhost:5000/stock/ratings/NASDAQ/' + this.stockSymbol)
      .pipe(map((response: any) =>  response));

  }

  aggregatedRatingForChart($ratingsModel): RatingsChartModel[] {

    let tempList: RatingsChartModel[] = [
      {value: 0, color: Constants.COLOR[2], size: '', legend: 'SELL'},
      {value: 0, color: Constants.COLOR[1], size: '', legend: 'HOLD'},
      {value: 0, color: Constants.COLOR[0], size: '', legend: 'BUY'},
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
