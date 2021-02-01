import React from 'react';
import { Route, Switch, NavLink, Link } from 'react-router-dom';
import { Container, Navbar } from 'react-bootstrap'; 
import { LinkContainer } from 'react-router-bootstrap';
import SignUp from './features/users/SignUp'
import LogIn from './features/users/LogIn'

import './App.css';

function App() {
  return (
    <>
      <Navbar bg='light' expand='lg' variant='light'>
        <LinkContainer to='/'>
          <Navbar.Brand className='logo'>Pizza</Navbar.Brand>
        </LinkContainer>
        <Navbar.Toggle />
        <Navbar.Collapse></Navbar.Collapse>
      </Navbar>
      <Container className='pt-3'></Container>
    <Switch>
      <Route exact path='/' render={() => (
        <div className='middle-center'>
          <h1 className='landing logo'>Pizza</h1>
          <Link className='btn btn-primary' to='/sign-up'>Sign up</Link>
          <Link className='btn btn-primary' to='/log-in'>Log in</Link>
        </div>
      )} />
      <Route path='/sign-up' component={SignUp} />
      <Route path='/log-in' component={LogIn} />
    </Switch>
    </>
  );
}

export default App;
