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
        var format_data = {
            date: new Date(Math.trunc(this.props.stock_data.timestamp * 1000)),
            AAPL: this.props.stock_data.average
        }
        return (
            <div>
                <Nav active='stock'/>
                <div className="container">
                    <div className="row">
                        <div className="col-md-8 col-md-offset-2">
                            <RTChart
                                fields={['AAPL']}
                                data={ format_data }
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