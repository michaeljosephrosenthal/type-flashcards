var React = require('react');
//window.React = React; 

var App = require('./App.jsx');
console.log(activePath);
React.render(<App url={"/api" + activePath} multi="true" />, document.getElementById('app'));
