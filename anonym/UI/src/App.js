import React from 'react';
import { Jumbotron } from 'reactstrap';
import { Button, Form, InputGroup, InputGroupAddon, Input } from 'reactstrap';
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
        {prop.meslog.map( mes =>   
          (
            <div>
              <img src={proPic} className="proPic" style={{visibility:mes.picVis}}/>
              <p className= {mes.messageType}>{mes.message}</p>
            </div>
            )
          )
      }
    </div>   
  )
}



class SendBar extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      counter: 0,
      text: ""
    }
  }

  onSubmit = e => {
    e.preventDefault();
    this.props.messageUpdater({messageType:"replyMessage",message:this.state.text, picVis:"hidden"})
    this.setState({text:""})
    
    
  }

  
  handleTextChange = e => {
    this.setState({text:e.target.value})
  }

  render() {
    return (
      <Form>
        <InputGroup className='textBox'>
          <Input type="text" name="message" value={this.state.text} onChange={this.handleTextChange} autoComplete="new-password"/>
          <InputGroupAddon addonType="append">
            <Button variant="primary" type="submit"
            onClick={e => this.onSubmit(e)}>Send</Button>
          </InputGroupAddon>
        </InputGroup>
      </Form> 
    );
  }
}




class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      messageLog: [
        {messageType:"chatMessage",message:"Hello, how can I assist you?", picVis:"visible"}
      ],
      counter:0
    };

    this.updateMessages = this.updateMessages.bind(this)
  }

  
  

  updateMessages(newMessage){

    let reply = null;

    switch(this.state.counter) {
      case 0:
        reply = {messageType:"chatMessage",message:"Can you tell me where it took place?", picVis:"visible"}
        break;
      case 1:
        reply = {messageType:"chatMessage",message:"Can you estimate the time when this happened?", picVis:"visible"}
        break;
      case 2:
        reply = {messageType:"chatMessage",message:"Was there anyone else present at the incident?", picVis:"visible"}
        break;
      case 3:
          reply = {messageType:"chatMessage",message:"Can you describe what they looked like?", picVis:"visible"}
        break;
      default:
        reply = {messageType:"chatMessage",message:"Can you give me more details?", picVis:"visible"}
        break;
    }

    this.setState({
      messageLog: [...this.state.messageLog,newMessage,reply],
      counter:this.state.counter+1
    })
  }

  render() {

    console.log(this.state)

    return (
      <div className="mainBody">
      <Header/>
        <Message meslog={this.state.messageLog} />
        <SendBar messageUpdater={this.updateMessages}/>
    </div>
    );
  }
}

export default App;
