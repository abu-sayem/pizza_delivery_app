import React from 'react'
import { Link } from 'react-router-dom'


const LogIn = (props) => {
  return (
    <>
      <Link to='/'>Home</Link>
      <h2>Log In</h2>
      <p>
        Don't have an account? <Link to='/sign-up'>Sign up!</Link>
      </p>
    </>
  )
}

export default LogIn
