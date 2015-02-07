var React = require('react');
var Router = require('react-router');

var Route = Router.Route;

var App = require('./App.jsx');

var Routes = (
  <Route handler={App} path="/">
  </Route>
);

module.exports = Routes;
