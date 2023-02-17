import React from 'react'
import './Notebook.scss'

const InitialBook = () => {
  return (
    <div className='notebook'>
      <img src={`https://ned-web-app.herokuapp.com/render/initial`} alt="Notebook" />
    </div>
  )
}

export default InitialBook