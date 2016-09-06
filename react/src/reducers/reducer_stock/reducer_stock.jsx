import { RECEIVED_STOCK_DATA } from '../../actions/action_stock/action_stock.jsx';

const initialState = null;

export default (state = initialState, action) => {
    switch(action.type) {
        case RECEIVED_STOCK_DATA:
            return action.payload;
    }
    return state;
}