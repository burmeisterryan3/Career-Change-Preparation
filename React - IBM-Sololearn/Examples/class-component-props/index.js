import React from 'react';
import ReactDOM from 'react-dom';
import './style.css';

// https://stackblitz.com/edit/react-class-component-props-example?file=index.js

class Hello extends React.Component {
  render() {
    return <p>Hello, {this.props.name}!</p>;
  }
}

const el = <Hello name="David" />; 
ReactDOM.render(
  el, 
  document.getElementById('root')
);