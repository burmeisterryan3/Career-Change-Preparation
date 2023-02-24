import React from 'react';
import ReactDOM from 'react-dom';
import './style.css';

// https://stackblitz.com/edit/react-functional-component-props-example?file=index.js

function Hello(props) {
  return <p>Hello, {props.name}!</p>;
}

const el = <Hello name="David" />; 
ReactDOM.render(
  el, 
  document.getElementById('root')
);