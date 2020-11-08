import {Component, OnChanges, OnInit} from '@angular/core';
import {RatingsService} from './services/ratings.service';
import {LogData} from './model/logData';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'SRE Stock Recommender Engine';
  lstLogs: LogData[];


  constructor(private ratingsService: RatingsService) {
  }

  ngOnInit(): void {
    this.ratingsService.getRatings()
      .subscribe(
        data => {
          this.lstLogs = data;
        }
      );
  }
}
