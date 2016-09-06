import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import socketio from 'socket.io-client';
var io = socketio.connect(`http://localhost:3001`);

import { received_stock_data } from '../../actions/action_stock/action_stock.jsx';

import Nav from '../../components/Nav.jsx';

class StockApp extends Component {
    componentDidMount() {

    }

    render() {
        io.on('stock-data', (stock_data) => {
            console.log(stock_data);
        });
        return (
            <div>
                <Nav active='stock'/>
                <div className="container">
                    <div className="row">
                        <div className="col-md-8 col-md-offset-2">

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