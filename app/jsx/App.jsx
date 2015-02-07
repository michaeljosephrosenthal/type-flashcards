var React = require('react');
var $ = require('jquery');

var Nav = require('./Nav.jsx');
var Word = require('./Word.jsx');


var App = React.createClass({
    getInitialState: function() {
        return {words: []};
    },
    componentDidMount: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: function(data) {
                this.setState(data);
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    render: function() {
        var Words = [];
        var ismulti = this.props.multi;
        this.state.words.forEach(function(word) {
            Words.push(
                <Word known={word[known]}
                    learning={word[learning]}
                    multi={ismulti}
                    key={Words.length}/>
            );
        });
        return (
            <div className="container">
                <Nav/>
                {Words}
            </div>
        );
    }
});

module.exports = App;
/*
   var Router = require('react-router');
   var RouteHandler = Router.RouteHandler;
   <RouteHandler/>
   */
