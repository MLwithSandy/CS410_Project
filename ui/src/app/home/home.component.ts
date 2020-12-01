import {AfterViewInit, Component, Input, OnInit, ViewChild} from '@angular/core';
import {LogData} from '../model/logData';
import {HttpClient} from '@angular/common/http';
import {map, startWith} from 'rxjs/operators';
import {RatingsModel} from '../model/ratings.model';
import {RatingsChartModel} from '../model/ratingsChart.model';
import {MatTableDataSource} from '@angular/material/table';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';
import {FormBuilder, FormControl, FormGroup} from '@angular/forms';
import {RatingsCardModel} from '../model/ratings-card.model';
import {Constants} from '../model/Constants.model';
import {TwitterSentiment} from '../model/twitter-sentiment.model';
import {StockListService} from '../services/StockList.Service';
import {RecommendationModel} from '../model/recommendation.model';
import {StockSectorModel} from '../model/stock-sector.model';
import {Observable} from 'rxjs';


declare var $: any;

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, AfterViewInit {

  stockSymbol = '';

  ratingsList: RatingsModel;

  ratingsCardModel: RatingsCardModel = new RatingsCardModel();
  sentimentCardModel: RatingsCardModel = new RatingsCardModel();
  overallCardModel: RatingsCardModel = new RatingsCardModel();

  recoList: RecommendationModel[] = [];
  stockSector: StockSectorModel;

  List: RatingsChartModel[] = [];

  dataSource = new MatTableDataSource();
  tweetList = new MatTableDataSource();

  stockListResponse: any = [];
  stockList: string[] = [];

  filteredStockList: Observable<string[]>;
  form: FormGroup;


  @ViewChild(MatPaginator, {static: false}) paginator: MatPaginator;
  @ViewChild(MatSort, {static: false}) sort: MatSort;

  displayedColumns = ['ratingDate', 'ratingAgency', 'ratingAssigned'];
  displayedColumnsTweets = ['Tweets'];

  constructor(private httpClient: HttpClient, private formBuilder: FormBuilder, private stockListService: StockListService) {

  }


  ngOnInit(): void {

    this.stockListService.getStockList().subscribe(
      data => {
        Object.assign(this.stockListResponse, data);
        this.stockList =  this.stockListResponse.map(x => x.Symbol
          + ' - '
          + (x['Security Name'].split('-'))[0]);

      },
      error => {
        console.log('Something wrong here');
      });


    this.form = this.formBuilder.group({
      stock: ['AAPL - Apple Inc.']
    });

    this.filteredStockList = this.form.get('stock').valueChanges.pipe(
      startWith(''),
      map(value => typeof value === 'string' ? value : value.name),
      map(name => name ? this._filter(name) : this.stockList.slice())
    );

    this.getSearchResult('AAPL');
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();
    // console.log('filtervalue: ', filterValue);
    // console.log('this.stockList: ', this.stockList);
    const filteredList = this.stockList.filter(option =>
      (option.toString().toLowerCase().indexOf(filterValue) === 0 || option.toString().toLowerCase().includes(filterValue)));

    // console.log('filteredList: ', filteredList);
    return filteredList;
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
    this.tweetList.paginator = this.paginator;
    this.tweetList.sort = this.sort;

  }

  getSearchResult(stockSearched: string): void {
    this.stockSymbol = (stockSearched.split('-'))[0];

    console.log('this.stockSymbol', this.stockSymbol);
    this.getStockRating().subscribe(
      result => {
        this.ratingsList = result[0];
        this.getRatingsCardStyle();
        this.getRatingForChart();
        this.prepareRatingDataTable();
      }
    );

    this.getSentiments().subscribe(
      res => {
        // console.log('res:', res);
        let senti;
        senti = new TwitterSentiment();
        senti.stockSymbol = res[0].stockSymbol;
        senti.refreshDate = res[0].refreshDate;
        senti.sentimentClass = res[0].sentiment;
        const index = Constants.SENTIMENT_SCALE.findIndex(x => x === res[0].sentiment);
        senti.sentiment = Constants.SENTIMENT[index];
        senti.tweets = [];
        for (let i = 0; i < res.length; i++) {
          senti.tweets[i] = res[i].tweets;
          // console.log('senti.tweets', senti.tweets[i]);
        }

        this.ratingsList.sentiment = new TwitterSentiment();
        this.ratingsList.sentiment =  senti;
        // console.log('this.ratingsList.sentiment: ', this.ratingsList.sentiment);

        this.tweetList.data = [];
        this.tweetList.data = this.ratingsList.sentiment.tweets;

        this.getSentimentCardStyle();
        this.getOverallRating();
        this.getOverallCardStyle();
      }
    );

    this.getRecommendationList().subscribe(
      res => {
        this.recoList = res;
        // console.log('this.recoList: ', this.recoList);
        for (let i = 0; i < this.recoList.length; i++) {
          this.recoList[i].bgImg = 'miscellaneous.jpg';
          if (this.recoList[i].sector !== '') {
            this.recoList[i].bgImg = this.recoList[i].sector.replace(/[^a-zA-Z0-9]/g, '').toLowerCase() + '.jpg';
          }
          this.recoList[i].cardImg = '/assets/images/' + this.recoList[i].rating + '.svg';
          this.recoList[i].btnColor =
            (this.recoList[i].rating === 'BUY' ? Constants.COLOR[0]
              : this.recoList[i].rating === 'HOLD' ? Constants.COLOR[1]
                : Constants.COLOR[2]);
        }
      }
    );
  }


  getRatingForChart(): void {
    this.List = this.aggregatedRatingForChart(this.ratingsList);
  }

  prepareRatingDataTable(): void {
    this.dataSource.data = [];

    this.dataSource.data = this.ratingsList.analystsRatings;
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
    // console.log(this.dataSource.data);
  }

  getRatingsCardStyle(): void {
    this.ratingsCardModel.imgPath = '/assets/images/' + this.ratingsList.overallRating + '.svg';
    this.ratingsCardModel.btnBgColor =
      (this.ratingsList.overallRating === 'BUY' ? Constants.COLOR[0]
        : this.ratingsList.overallRating === 'HOLD' ? Constants.COLOR[1]
          : Constants.COLOR[2]);
  }

  getSentimentCardStyle(): void {
    const index = Constants.SENTIMENT.findIndex(x => x === this.ratingsList.sentiment.sentiment);
    this.sentimentCardModel.imgPath = '/assets/images/' + this.ratingsList.sentiment.sentiment + '.svg';
    this.sentimentCardModel.btnBgColor = Constants.COLOR[index];
  }

  getOverallRating(): void {

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

  getOverallCardStyle(): void {
    this.overallCardModel.imgPath = '/assets/images/' + this.ratingsList.combinedRating + '.svg';
    this.overallCardModel.btnBgColor =
      (this.ratingsList.combinedRating === 'BUY' ? Constants.COLOR[0]
        : this.ratingsList.combinedRating === 'HOLD' ? Constants.COLOR[1]
          : Constants.COLOR[2]);
  }

  getStockRating(): any {

    // this.ratingsList = [];

    // console.log('stockSymbol: ' + this.stockSymbol  );
    return this.httpClient
      .get('http://localhost:5000/stock/ratings/NASDAQ/' + this.stockSymbol)
      .pipe(map((response: any) => response));

  }

  getSentiments(): any {

    // console.log('stockSymbol: ' + this.stockSymbol  );
    return this.httpClient
      .get('http://localhost:5000/stock/sentiments/NASDAQ/' + this.stockSymbol)
      .pipe(map((response: any) => response));

  }

  getRecommendationList(): any {

    console.log('stockSymbol: ' + this.stockSymbol);
    return this.httpClient
      .get('http://localhost:5000/stock/recommendation/' + this.stockSymbol)
      .pipe(map((response: any) => response));

  }

  aggregatedRatingForChart($ratingsModel): RatingsChartModel[] {

    let tempList: RatingsChartModel[] = [
      {value: 0, color: Constants.COLOR[2], size: '', legend: 'SELL'},
      {value: 0, color: Constants.COLOR[1], size: '', legend: 'HOLD'},
      {value: 0, color: Constants.COLOR[0], size: '', legend: 'BUY'},
    ];

    // Calculate the sums and group data (while tracking count)
    const reduced = $ratingsModel.analystsRatings.reduce((m, d) => {
      if (!m[d.scaledRatings]) {
        m[d.scaledRatings] = {rating: d.scaledRatings, count: 1};
        return m;
      }
      m[d.scaledRatings].count += 1;

      return m;
    }, {});

    for (const x in reduced) {
      if (x === 'BUY') {
        tempList[2].value = reduced[x].count;
      }
      if (x === 'HOLD') {
        tempList[1].value = reduced[x].count;
      }
      if (x === 'SELL') {
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
