import { combineReducers } from 'redux';

import VideosReducer from './reducer_video/reducer_videos.jsx';
import ActiveVideoReducer from './reducer_video/reducer_active_video.jsx';

import WeatherReducer from './reducer_weather/reducer_city_weather.jsx';

import StockReducer from './reducer_stock/reducer_stock';


const rootReducer = combineReducers({
    videos: VideosReducer,
    activeVideo: ActiveVideoReducer,
    
    weather: WeatherReducer,
    
    stock_data: StockReducer
});

export default rootReducer;