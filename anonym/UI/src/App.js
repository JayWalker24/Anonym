import React from 'react';
import { Jumbotron } from 'reactstrap';
import {Alert, Button, Form, InputGroup, InputGroupAddon, Input } from 'reactstrap';
import axios from 'axios';
import proPic from './silhoe.jpg';
import './App.css';


/*
Things to do: Add Unique Key prop for each message, make messages type out instead of 
appreading automatically, add an alt prop to each img, put messages in row object to fix formatting.
Replace the submission alert with a modal
*/

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
      counter: 0,
      complete: 1
    };
    this.updateMessages = this.updateMessages.bind(this)
  }

  finalSubmit = e => {
    console.log("Report Submitted")
    const info = this.state.messageLog
    let today = new Date();
    let date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    let report = {
        "lines" : [],
        "mail_record_to" : "12 Bedford Ave, Brooklyn, NY, 11203", 
        "date_report" : date, 
        "time_report": time, 
        "date_crime" : info[5].message, 
        "location_crime" : info[9].message, 
        "time_crime" : info[7].message, 
        "crime_description" : info[3].message, 
        "suspect_description" : info[13].message
    }
    this.setState({
      complete: 2
    })
    console.log(report)

    axios.post(`http://localhost:5000/api`, { report })
            .then(res => {
                console.log(res);
                console.log(res.data);
        })
  }
  

  updateMessages(newMessage){

    let reply = null;

    switch(this.state.counter) {
      case 0:
        reply = {messageType:"chatMessage",message:"What type of incident was it?", picVis:"visible"}
        break;
      case 1:
        reply = {messageType:"chatMessage",message:"What was that date that this occured?", picVis:"visible"}
        break;
      case 2:
        reply = {messageType:"chatMessage",message:"What was the approximate time of the incident?", picVis:"visible"}
        break;
      case 3:
          reply = {messageType:"chatMessage",message:"And where did it take place?", picVis:"visible"}
        break;
      case 4:
        reply = {messageType:"chatMessage",message:"Was there anyone else present?", picVis:"visible"}
        break;
      case 5:
        reply = {messageType:"chatMessage",message:"Can you give a description of what they looked like?", picVis:"visible"}
        break;
      default:
        reply = {messageType:"chatMessage",message:"The report is complete to be submitted", picVis:"visible"}
        break;
    }

    this.setState({
      messageLog: [...this.state.messageLog,newMessage,reply],
      counter:this.state.counter+1
    })
  }

  render() {

    if(this.state.complete===0){
      return (
        <div className="mainBody">
          <Header/>
          <Message meslog={this.state.messageLog} />
          <SendBar messageUpdater={this.updateMessages}/>
          <Button color="danger" size="lg" disabled>Submit Report</Button>
        </div>
        );
    } else if(this.state.complete===1){
      return (
        <div className="mainBody">
          <Header/>
          <Message meslog={this.state.messageLog} />
          <SendBar messageUpdater={this.updateMessages}/>
          <Button color="danger" size="lg" active onClick={e => this.finalSubmit(e)}>Submit Report</Button>
        </div>
        );
    }else if(this.state.complete===2){
      return (
        <div className="mainBody">
          <Alert color="success">
            Report has been sent successfully
          </Alert>
        </div>
        );
    }
      
  }
}

export default App;
