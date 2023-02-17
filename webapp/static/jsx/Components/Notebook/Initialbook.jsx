import React from 'react'
import './Notebook.scss'

const InitialBook = () => {
  return (
    <div className='notebook'>
      <img src={`http://127.0.0.1:5000/render/initial`} alt="Notebook" />
    </div>
  )
}

export default InitialBook