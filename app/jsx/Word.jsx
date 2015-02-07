var React = require('react');

var Retries = React.createClass({
    render: function() {
        count = (4 - this.props.tries % 4) % 4;
        if (count > 0) {
            var span = "";
            if (count == 3 ) {
                span = <span className="three">3x</span>;
            }
            else if (count == 2 ) {
                span = <span className="two">2x</span>;
            }
            return (
                <div className="retries">
                    {span}
                    <button className="btn btn-lg btn-danger flasher">{ this.props.learning }</button>
                </div>
            );
        } else { return <div/>; }
    }
});

var Word = React.createClass({
    getInitialState: function() {
        return {
            tries: 0,
            attempted: false,
            success: false,
            stateClass: ""
        };
    },
    addSuccessScroll: function(){
        node = this.refs.form.getDOMNode();
        this.setState({
            success: true,
            attempted: true,
            stateClass: "success"
        });
        flash("success");
        $('html body').animate({
            scrollTop: $(node).offset().top
        }, 500);
        $(node).next().find('input[name="guess"]').focus();
    },
    correctRetry: function(){
        this.setState({
            tries: this.state.tries+1,
            stateClass: "warning"
        });
        this.refs.guess.getDOMNode().value = "";
        flash("warning");
    },
    wrong: function(){
        tries = this.state.tries;
        this.setState({
            tries: tries+1,
            success: false,
            attempted: true,
            stateClass: "danger"
        });
        flash("danger");
    },
    handleSubmit: function(event){
        event.preventDefault();
        var answer  = this.refs.learning.getDOMNode().value.trim(),
            guess   = this.refs.guess.getDOMNode().value.trim(),
            tries   = this.state.tries;
        speak(answer);
        if(tries % 3 === 0 && guess == answer){
            this.addSuccessScroll();
        } else if (guess == answer){
            this.correctRetry();
        } else {
            this.wrong();
        }
    },
    render: function() {
        var tags = [];
        var ismulti = this.props.multi;
        if (ismulti) {
            this.props.known.forEach(function(alt){
                tags.push(<li><button className="btn btn-sm btn-default" type="button">{alt}</button></li>);
            });
            append = <ul className="col-sm-offset-3 list-inline alts">
                {tags}
            </ul>;
        }
        return (
            <form className={"read form-horizontal flasher " + this.state.stateClass}
                  onSubmit={this.handleSubmit} ref="form">
                <input type="hidden" ref="learning" className="form-control" value={this.props.learning}/>
                <div className="form-group">
                    <label className="col-sm-3 control-label">{ ismulti ? this.props.known[0] : this.props.known }:</label>
                    <div className="col-sm-7">
                        <input type="text" name="guess" ref="guess" className="form-control input-lg flasher" autoComplete="off" />
                    </div>
                    <Retries tries={this.state.tries} learning={this.props.learning} />
                    <button type="submit" className="btn btn-lg btn-primary">Enter</button>
                    {append}
                </div>
            </form>
        );
    }
});
module.exports = Word;
