var React = require('react');

var Retries = React.createClass({
    render: function() {
        count = 3 - this.props.correctTries;
        if (this.props.wrongTries && count) {
            return (
                <div className="retries">
                    { count > 1 ? <span className="count">{count}x</span> : "" }
                    <button className="btn btn-lg btn-danger flasher">{ this.props.learning }</button>
                </div>
            );
        } else { return <div/>; }
    }
});

var Word = React.createClass({
    getInitialState: function() {
        return {
            wrongTries: 0,
            correctTries: 0,
            success: false,
            stateClass: "",
            guess: ""
        };
    },
    addSuccessScroll: function(){
        node = this.refs.form.getDOMNode();
        this.setState({
            success: true,
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
            correctTries: this.state.correctTries + 1,
            stateClass: "warning",
            guess: ""
        });
        flash("warning");
    },
    wrong: function(){
        this.setState({
            wrongTries: this.state.wrongTries + 1,
            success: false,
            stateClass: "danger",
            guess: ""
        });
        flash("danger");
    },
    handleSubmit: function(event){
        event.preventDefault();
        var answer = this.props.learning,
            guess  = this.state.guess,
            correctTries  = this.state.correctTries;
            wrongTries  = this.state.wrongTries;
        speak(answer);
        if (guess == answer &&
            (wrongTries === 0 ||
             (this.state.correctTries - 2 === 0 ))) {
            this.addSuccessScroll();
        } else if (guess == answer){
            this.correctRetry();
        } else {
            this.wrong();
        }
    },
    handleGuessChange: function(event) {
        this.setState({ guess: event.target.value });
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
                <div className="form-group">
                    <label className="col-sm-3 control-label">{ ismulti ? this.props.known[0] : this.props.known }:</label>
                    <div className="col-sm-7">
                        <input type="text" name="guess" ref="guess" value={this.state.guess} onChange={this.handleGuessChange}
                            className="form-control input-lg flasher" autoComplete="off" />
                    </div>
                    <Retries correctTries={this.state.correctTries}
                        wrongTries={this.state.wrongTries}
                        learning={this.props.learning} />
                    <button type="submit" className="btn btn-lg btn-primary">Enter</button>
                    {append}
                </div>
            </form>
        );
    }
});
module.exports = Word;
