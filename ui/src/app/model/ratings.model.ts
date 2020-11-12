import {AnalystsRating} from './analystsRating';

export class RatingsModel{
  index: number;
  stockSymbol: string;
  marketPlace: string;
  refreshData: string;
  overallRating: string;
  analystsRatings: AnalystsRating[];
}
