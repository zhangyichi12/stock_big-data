import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { received_stock_data } from '../../actions/action_stock/action_stock.jsx';

import socketio from 'socket.io-client';
import RTChart from 'react-rt-chart';

import Nav from '../../components/Nav.jsx';

var io = socketio.connect(`http://localhost:3001`);

class StockApp extends Component {
    componentDidMount() {
        io.on('stock-data', (stock_data) => {
            let parsed_data = JSON.parse(stock_data);
            this.props.received_stock_data(parsed_data);
        });
    }

    render() {
        let stock_symbol = 'NASDAQ(.IXIC)';
        let format_data = {
            date: new Date(Math.trunc(this.props.stock_data.timestamp * 1000)),
            // GOOGL: this.props.stock_data.average
        }
        let stock_price = this.props.stock_data.average
        if(stock_price) {
            stock_price = Number(stock_price.toFixed(3));
        }
        format_data[stock_symbol] = stock_price
        console.log(stock_price);
        return (
            <div>
                <Nav active='stock'/>
                <div className="container">
                    <div className="row">
                        <div className="col-md-8 col-md-offset-2">
                            <RTChart
                                fields = {[ stock_symbol ]}
                                data = { format_data }
                                maxValues = { 1000 }
                                flow = { {duration: 200} }
                            />
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-8">

                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        stock_data: state.stock_data
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators({ received_stock_data }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(StockApp);