export const RECEIVED_STOCK_DATA = 'RECEIVED_STOCK_DATA';

export function received_stock_data(stock_data) {
    return {
        type: RECEIVED_STOCK_DATA,
        payload: stock_data
    }
}