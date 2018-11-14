import React from 'react';
import ReactDOM from 'react-dom';
// import '@atlaskit/css-reset';
import App from './app.jsx';

window.React = React;
window.ReactDOM = ReactDOM;
window.App = App;

//Puts the App into the DOM
ReactDOM.render(<App />, document.getElementById('root'));