import React from 'react';
import { Jumbotron } from 'reactstrap';
import { InputGroup, InputGroupText, InputGroupAddon, Input } from 'reactstrap';
import proPic from './silhoe.jpg';
import './App.css';

const Header = () => {
  return (
    <Jumbotron>
      <h1 className="display-5">Welcome to Anonym, type below to start the conversation</h1>
      <p className="lead">The completely anonymous police report compiler.</p>
    </Jumbotron>
  )
}


const Message = (prop) => {
  return(
    <div>
    </div>
  )
}

function App() {
  return (
    <div className="mainBody">
      <Header/>
        <img src={proPic} className="proPic" />
        <p className="chatMessage">Hello how are you doing?</p>    
        <br></br>  
        <p className="replyMessage">I just witnessed a crime and would like to report it</p>   
        <InputGroup className='textBox'>
          <Input />
          <InputGroupAddon addonType="append">
            <InputGroupText>Send</InputGroupText>
          </InputGroupAddon>
        </InputGroup>
    </div>
  );
}

export default App;
