import React from 'react';
import ReactDOM from 'react-dom';
import './style.css';

// https://stackblitz.com/edit/react-state-counter-example?file=index.js

class Counter extends React.Component {
  state = {
    counter: 0
  }
  increment = () => {
    this.setState({counter: this.state.counter+1});
  }
  // Sets initial value of counter to 42
  componentDidMount() {
    this.setState({counter: 42});
  }
  render() {
    return <div>
    <p>{this.state.counter}</p>
    <button onClick={this.increment}>Increment</button>
    </div>;
  }
}

const el = <Counter />; 
ReactDOM.render(
  el, 
  document.getElementById('root')
);