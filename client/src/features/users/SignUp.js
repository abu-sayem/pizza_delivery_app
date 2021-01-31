import React from 'react'
import { Link } from 'react-router-dom'


const Signup = (props) => {
  return (
    <>
      <Link to='/'>Home</Link>
      <h2>Signup</h2>
      <p>
        Already have an account? <Link to='/log-in'>Log in!</Link>
      </p>
    </>
  )
}

export default Signup
