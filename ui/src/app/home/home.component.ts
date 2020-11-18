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
import {TwitterSentiment} from '../model/twitter-sentiment.model';
import {StockListService} from '../services/StockList.Service';
import {RecommendationModel} from '../model/recommendation.model';

declare var $: any;


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, AfterViewInit {

  lstLogs: LogData[];

  stockList: any[] = [];
  stockList2: any;


  @Input()
  stockSymbol;

  // ratingsList: RatingsModel[];

  ratingsList: RatingsModel;
  ratingsCardModel: RatingsCardModel;
  sentimentCardModel: RatingsCardModel;
  overallCardModel: RatingsCardModel;

  recoList: RecommendationModel[];

  lastkeydown1 = 0;
  lastkeydown2 = 0;
  subscription: any;

  List: RatingsChartModel[];

  dataSource = new MatTableDataSource();

  @ViewChild(MatPaginator, { static: false }) paginator: MatPaginator;
  @ViewChild(MatSort, { static: false }) sort: MatSort;

  // displayedColumns = ['ratingDate', 'stockSymbol', 'ratingAgency', 'ratingAssigned'];
  displayedColumns = ['ratingDate', 'ratingAgency', 'ratingAssigned'];

  constructor(private httpClient: HttpClient, private stockListService: StockListService) {
    // Get the user data from users.json
    this.stockListService.getStockList().subscribe(
      data => {
        Object.assign(this.stockList, data);
        // console.log('data: ', data);
        console.log('this.stockList: ', this.stockList);
      },
      error => {
        console.log('Something wrong here');
      });
  }


  ngOnInit(): void {
    $('#stockSymbol').autocomplete({
      source: this.stockList
    });

    this.ratingsCardModel = new RatingsCardModel();
    this.sentimentCardModel = new RatingsCardModel();
    this.overallCardModel = new RatingsCardModel();
    this.ratingsList = new RatingsModel();
    this.ratingsList.sentiment = new TwitterSentiment();
    this.ratingsList.analystsRatings = [];
    this.recoList = [];
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

  // tslint:disable-next-line:typedef
  getStockSymbol($event) {

    const stockId = (document.getElementById('dynamicUserIdsSecondWay') as HTMLInputElement).value;

    if (stockId.length > 2) {
      if ($event.timeStamp - this.lastkeydown2 > 200) {
        this.stockList2 = this.searchFromArray(this.stockList, stockId);

        $('#stockSymbol').autocomplete({
          source: this.stockList2,
          messages: {
            noResults: '',
            results(): void { }
          }
        });
      }
    }
  }

  // tslint:disable-next-line:typedef
  searchFromArray(arr, regex) {
    let matches = [], i;
    for (i = 0; i < arr.length; i++) {
      if (arr[i].match(regex)) {
        matches.push(arr[i]);
      }
    }
    return matches;
  }


 getSearchResult(): void{
   this.stockSymbol = (document.getElementById('stockSymbol') as HTMLInputElement).value.split(':')[0];

   console.log('this.stockSymbol', this.stockSymbol);
   this.getStockRating().subscribe(
    // this.getCombinedRating().subscribe(
      result => {

        // const testM: RatingsModel[] = result.analyst;
        // console.log('result.analyst[0]', testM);
        // console.log('result.sentiment', result.sentiment);


        // console.log('testM', this.ratingsList);

        this.ratingsList = result[0];
        this.getRatingsCardStyle();
        this.getRatingForChart();
        this.prepareRatingDataTable();

        this.getSentiments().subscribe(
          res => {
              const senti = new TwitterSentiment();
              senti.stockSymbol = res.stockSymbol;
              senti.refreshDate = res.refreshDate;
              senti.sentimentClass = res.sentiment;
              senti.sentiment = Constants.SENTIMENT[3 - senti.sentimentClass];
              this.ratingsList.sentiment = senti;
              this.getSentimentCardStyle();
              this.getOverallRating();
              this.getOverallCardStyle();
          }
        );
        this.getRecommendationList().subscribe(
          res => {
            this.recoList = res;
            console.log('res: ' , res);
            console.log('this.recolist: ', this.recoList);
          }
        );

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

  getSentimentCardStyle(): void{
    const scaledSenti = 3 - this.ratingsList.sentiment.sentimentClass;
    this.sentimentCardModel.imgPath = '/assets/images/' + Constants.SENTIMENT[scaledSenti] + '.svg';
    this.sentimentCardModel.btnBgColor = Constants.COLOR[scaledSenti];
  }

  getOverallRating(): void{

    let index = Constants.SENTIMENT.findIndex(x => x === this.ratingsList.sentiment.sentiment);
    const tempSentiment = Constants.SENTIMENT_SCALE[index];

    index = Constants.RATING.findIndex(x => x === this.ratingsList.overallRating);
    const tempRating = Constants.RATING_SCALE[index];

    const resultRating = (tempSentiment + tempRating > 1 ? tempSentiment + tempRating - 1
                          : tempSentiment + tempRating < -1 ? tempSentiment + tempRating + 1
                          : tempSentiment + tempRating);

    index = Constants.RATING_SCALE.findIndex(x => x === resultRating);
    this.ratingsList.combinedRating = Constants.RATING[index];
  }

  getOverallCardStyle(): void{
    this.overallCardModel.imgPath = '/assets/images/' + this.ratingsList.combinedRating + '.svg';
    this.overallCardModel.btnBgColor =
      (this.ratingsList.combinedRating === 'BUY' ? Constants.COLOR[0]
        : this.ratingsList.combinedRating === 'HOLD' ? Constants.COLOR[1]
          : Constants.COLOR[2]);
  }

  getStockRating(): any{

    // this.ratingsList = [];

    console.log('stockSymbol: ' + this.stockSymbol  );
    return this.httpClient
      .get('http://localhost:5000/stock/ratings/NASDAQ/' + this.stockSymbol)
      .pipe(map((response: any) =>  response));

  }

  getCombinedRating(): any{

    // this.ratingsList = [];

    console.log('stockSymbol: ' + this.stockSymbol  );
    return this.httpClient
      .get('http://localhost:5000/stock/ratings/combined/NASDAQ/' + this.stockSymbol)
      .pipe(map((response: any) =>  response));

  }

  getSentiments(): any{

    console.log('stockSymbol: ' + this.stockSymbol  );
    return this.httpClient
      .get('http://localhost:5000/stock/sentiments/NASDAQ/' + this.stockSymbol)
      .pipe(map((response: any) =>  response));

  }

  getRecommendationList(): any{

    console.log('stockSymbol: ' + this.stockSymbol  );
    return this.httpClient
      .get('http://localhost:5000/stock/recommendation/' + this.stockSymbol)
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
