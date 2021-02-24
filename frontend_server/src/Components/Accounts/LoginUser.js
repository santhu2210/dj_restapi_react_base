
import React, { Component } from 'react'
import {Row} from 'reactstrap';
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "./Login.css";


class LoginUser extends Component {
    constructor(props) {
        super(props)
        this.state = {
            password : ''
        }
    }
    handlePasswordChange = (e) => {
        this.setState({
            password : e.target.value
        })
    }
    render() {
        return (
            <div >
                <Form onSubmit={e => this.props.handleLogin(e, {
                    username : this.props.username, 
                    password : this.state.password
                })} >
                    <Form.Group>
                        <label htmlFor="username" >Username</label>
                        <input type="text"
                        onChange={this.props.handleLoginChange} 
                        value={this.props.username} 
                        name="username"
                        id="username"
                        placeholder="Username" />
                    </Form.Group>
                    <Form.Group>
                        <label htmlFor="password" >Password</label>
                        <input type="password"
                        onChange={this.handlePasswordChange} 
                        value={this.state.password} 
                        name="password"
                        id="password"
                        placeholder="Password" />
                    </Form.Group>
                    <Button type='submit'>Login</Button>
                </Form>
            </div>
        )
    }
}

export default LoginUser