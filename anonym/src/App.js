import React from 'react';
import logo from './priv.png';
import './App.css';
import Form from './Form'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo}/>
        <p>
          Welcome to Anonym.
        </p>
        <h1>
          Bruh
        </h1>
        <Form/>
        
      </header>
    </div>
  );
}

export default App;
