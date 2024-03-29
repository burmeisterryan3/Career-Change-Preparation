import React from 'react';
import ReactDOM from 'react-dom';
import './style.css';

// https://stackblitz.com/edit/react-state-initial-example?file=index.js

class Hello extends React.Component {
  state = {
    name: "James"
  }
  render() {
    return <h1>Hello {this.state.name}.</h1>;    
  }
}

const el = <Hello />; 
ReactDOM.render(
  el, 
  document.getElementById('root')
);