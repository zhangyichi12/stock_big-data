import { RECEIVED_STOCK_DATA } from '../../actions/action_stock/action_stock.jsx';

const initialState = [];

export default (state = initialState, action) => {
    switch(action.type) {
        case RECEIVED_STOCK_DATA:
            // let currentState = state;
            // let array_stock_data = [...currentState, action.payload.average + 50];
            // while(array_stock_data.length > 20) {
            //     array_stock_data.shift();
            // }
            // console.log(array_stock_data);
            return action.payload;
    }
    return state;
}