import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import './style.css';

// https://stackblitz.com/edit/react-hooks-counter-example?file=index.js

function Counter() {
  const [counter, setCounter] = useState(0);

  function increment() {
    setCounter(counter+1);
  }
  return <div>
  <p>{counter}</p>
  <button onClick={increment}>Increment</button>
  </div>;
}

const el = <Counter />; 
ReactDOM.render(
  el, 
  document.getElementById('root')
);