var React = require('react');

var NavItem = React.createClass({
    render: function() {
        return (
            <li className={this.props.href == activePath ? "active" : ""}>
                <a href={this.props.href}>{this.props.text}</a>
            </li>
        );
    }
});
var Nav = React.createClass({
    render: function() {
        return (
            <nav className="navbar navbar-default">
                <div className="container-fluid">
                    <div className="navbar-header">
                        <a className="navbar-brand" href="/">Type Flashcards</a>
                    </div>
                    <div>
                        <ul className="nav navbar-nav">
                            <NavItem href="/thai/to/eng" text="Thai to English" />
                            <NavItem href="/eng/to/thai" text="English to Thai" />
                            <NavItem href="/ukr/to/eng" text="Ukrainian to English" />
                            <NavItem href="/create/wordlist" text="Create WordList" />
                        </ul>
                    </div>
                </div>
            </nav>
        );
    }
});

module.exports = Nav;
