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

let report = {
    "mail_record_to": "",
    "date_report": "",
    "time_report": "",
    "date_crime": "",
    "location_crime": "",
    "time_crime": "",
    "crime_description": "",
    "suspect_description": ""
}

let questions = {
  "Can you give more information on the crime itself?":0,
  "Can you give a full detailed report of the suspect(s)":0,
  "Do you know the exact date/time and can you write it in the following format: Day/Month/Year Hour:Minutes AM/PM? (Example: 1/8/2019 3:45 AM)":0,
  "Can you give me an exact address?":0
}

let questions2 = [
  {question:"Can you briefly describe what happened?",value:0},
  {question:"Was there anyone else present who you believe may be responsible?",value:0},
  {question:"Can you estimate when these events occured",value:0},
  {question:"Where did this happen?",value:0}
]

let previousResponse = ""

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
    
    const sendMessage = {
      "message": this.state.text
    }
    const sendText = this.state.text
    let recording = false
    switch(previousResponse) {
      case "Can you give more information on the crime itself?":
        report["crime_description"]=sendText
        questions2[0].value = 1
        recording = true
        break;
      case "Can you give a full detailed report of the suspect(s)":
        report["suspect_description"]=sendText
        questions2[1].value = 1
        recording = true
        break;
      case "Do you know the exact date/time and can you write it in the following format: Day/Month/Year Hour:Minutes AM/PM? (Example: 1/8/2019 3:45 AM)":
        report["date_crime"]=sendText
        questions2[2].value = 1
        recording = true
        break;
      case "Can you give me an exact address?":
        report["location_crime"]=sendText
        questions2[3].value = 1
        recording = true
        break;
      default: 
        break;
    }
    if (recording){
      let recordingReply = questions2.find(item => item.value == 0)
      if(recordingReply!=undefined){
        this.props.messageUpdater({messageType:"replyMessage",message:sendText, picVis:"hidden"},{messageType:"chatMessage",message:recordingReply.question, picVis:"visible"})
        previousResponse = ""
      }else{
        this.props.messageUpdater({messageType:"replyMessage",message:sendText, picVis:"hidden"},{messageType:"chatMessage",message:"Report has been completed", picVis:"visible"})
        previousResponse = ""
      }

    }else{
      axios.post(`http://localhost:5000/message`, { sendMessage })
            .then(res => {
                this.props.messageUpdater({messageType:"replyMessage",message:sendText, picVis:"hidden"},{messageType:"chatMessage",message:res.data.answer, picVis:"visible"})
                previousResponse = res.data.answer
        })
    }
    
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
      complete: 0
    };
    this.updateMessages = this.updateMessages.bind(this)
  }

  finalSubmit = e => {
    let today = new Date();
    let date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    report.mail_record_to = "12 Bedford Ave, Brooklyn, NY, 11203"
    report.date_report = date
    report.time_report = time
    let crime_date = report.date_crime
    report.date_crime = crime_date.substring(0,7)
    report.time_crime = crime_date.substring(9,16)
    this.setState({
      complete: 2
    })
    console.log(report)
    axios.post(`http://localhost:5000/api`, report )
            .then(res => {
                console.log(res);
                console.log(res.data);
        })
  }
  

  updateMessages(oldMessage, newMessage){
    if(newMessage.message=="Report has been completed"){
      this.setState({
        messageLog: [...this.state.messageLog,oldMessage,newMessage],
        complete: 1
      })
    }else{
      this.setState({
        messageLog: [...this.state.messageLog,oldMessage,newMessage],
      })
    }
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
