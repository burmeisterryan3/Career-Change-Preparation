import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import './style.css';

// https://stackblitz.com/edit/react-simple-list-example?file=index.js

function MyList(props) {
  const arr = props.data;
  const listItems = arr.map((val) =>
    <li>{val}</li>
  );
  return <ul>{listItems}</ul>;
}

const arr = ["A", "B", "C"];
const el = <MyList data={arr} />; 

ReactDOM.render(
  el, 
  document.getElementById('root')
);