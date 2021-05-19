import React, {useState, useEffect} from 'react';
import {BrowserRouter as Router, Route, Link, useLocation} from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import Login from './pages/Login/Login';
import Home from './pages/Home/Home';

const App = () => {

  const [currentTime, setCurrentTime] = useState(0);
  useEffect(() => {
    fetch('/time').then(res => res.json())
      .then(data => {
        setCurrentTime(data.time);
      })
  },[])

  return (
    <Router>
      <Route path="/" exact component={Login} />
      <Route path="/home" exact component={Home} />
    </Router>
  );
}

export default App;
