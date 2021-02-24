
import React, { Component } from 'react'
import Axios from 'axios';
import {Row} from 'reactstrap';
const required = (val) => val && val.length;
const minLength = (len, val) => !(val) || (val.length < len);
const maxLength = (len, val) => (val.length > len);
const isEqual = (p1, p2) => p1 === p2

const base_url = window.SERVER_ADDRESS
class EditUser extends Component {
    constructor(props) {
        super(props)
    
        this.state = {
            full_name : '',
            telephone : '',
            email : '',
            display_full_name : false,
            display_telephone : false,
            display_email : false,
        }

    }

      componentDidMount(){
        // debugger;        
 //       if(this.state.logged_in){
          fetch(base_url + 'user-profile', {
            method : 'GET',
            headers : {
              Authorization : `JWT ${localStorage.getItem('token')}`
            }
          })
          .then(res => res.json())
          .then(resp => {
            this.setState({ full_name : resp.data[0].name, telephone: resp.data[0].telephone, email:resp.data[0].email })
          })
          .catch(err => console.log(err));
      //  }
      }


    getErrors = (name, value) => {
        let errors = [];
        if(!required(value)){
            errors.push('This value is required')
        }
        if(minLength(4, value)){
            errors.push('Greater than 4 characters required')
        }
        if(maxLength(25, value)){
            errors.push('Cannot be more than 25 characters')
        }
        const property = 'display_' + name
        if(errors.length === 0){
            // this.setState({
            //     [property] : false
            // })
            this.state[property] = false
        }
        if(this.state[property]){
            return (<>{errors.map((error,index) => <Row key={index} style={{color : 'red'}}>{error}</Row>)}</>)        
        }
    }
    isValid = () => {
        let valid = true;
        Object.values(this.state).forEach((val) => {
                if(val === true){
                    valid = false
                    return valid
                }
        })
        return valid;
    }

    clearForm = () => {
        this.setState({
            full_name : '',
            telephone : '',
            email : '',
            display_full_name : false,
            display_telephone : false,
            display_email : false,
        })
    }
    editUserProfile = e => {
        e.preventDefault()
        const {full_name, telephone, email} = this.state
        if(this.isValid()){
            Axios.put(base_url + 'user-profile/edit', {
                'profile' : {
                    'name' : full_name,
                    'telephone' : telephone,
                    'email' :  email
                }
            },
            {
                headers : {
                  Authorization : `JWT ${localStorage.getItem('token')}`
                }

            })
            .then(response => {
                console.log(response)
                console.log(response.status + " " + response.statusText)
            })
            .catch(error => {
                console.log(error)
            })
            this.clearForm()
        }
                
    }
    
    changeHandler = (event) => {
        event.preventDefault()
            var stateObject = function() {
              var returnObj = {};
              returnObj['display_' + event.target.name] = true;
                 return returnObj;
            }();
        
            this.setState( stateObject );    
            this.setState({
                [event.target.name] : event.target.value,
            })
        }
        
    render() {
        return (
            <div>
                <form onSubmit={this.editUserProfile} noValidate>
                    <div>
                        <label htmlFor="full_name"> Full name </label>
                        <input type="text" id="full_name" name="full_name" value={this.state.full_name} onChange={this.changeHandler}  />
                        {this.getErrors('full_name', this.state.full_name)}
                    </div>
                    <div>
                        <label htmlFor="telephone"> Telephone </label>
                        <input type="text" id="telephone" name="telephone" value={this.state.telephone} onChange={this.changeHandler}  />
                        {this.getErrors('telephone', this.state.telephone)}
                    </div>
                    <div>
                        <label htmlFor="email"> Email </label>
                        <input type="text" id="email" name="email" value={this.state.email} onChange={this.changeHandler}  />
                        {this.getErrors('email', this.state.email)}
                    </div>

                    <button type='submit'>Update</button>
                </form>    
            </div>
        )
    }
}

export default EditUser