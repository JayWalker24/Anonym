import React from 'react';

export default class Form extends React.Component {


    state = {
        firstName: '',
        lastName: '',
        callReason:''
    }


    onSubmit = e => {
        e.preventDefault();
        console.log(this.state)
    }

    render(){
        return(
            <form>
                <input placeholder='First Name' 
                value = {this.state.firstName}
                onChange = {e => this.setState({firstName: e.target.value})}
                />
                    <br/>
                <input placeholder='Last Name' 
                value = {this.state.lastName}
                onChange = {e => this.setState({lastName: e.target.value})}
                />
                    <br/>
                <input placeholder='Reporting' 
                value = {this.state.callReason}
                onChange = {e => this.setState({callReason: e.target.value})}
                />
                    <br/>
                <button onClick={e => this.onSubmit(e)}>Submit</button>
            </form>
        )
    }
}