import {AnalystsRating} from './analystsRating';
import {TwitterSentiment} from './twitter-sentiment.model';

export class RatingsModel{
  index: number;
  stockSymbol: string;
  marketPlace: string;
  refreshData: string;
  overallRating: string;
  combinedRating: string;
  sentiment: TwitterSentiment;
  analystsRatings: AnalystsRating[];
}
