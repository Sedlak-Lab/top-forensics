import React from 'react'
import './Notebook.scss'

const Notebook = ({notebook}) => {
  const filename = notebook[0].name
  console.log(filename)


  return (
    <div className='render'>
      <div className='notebook'>
        <img src={`https://ned-web-app.herokuapp.com/render/${filename}?${Date.now()}`} alt="Notebook" />
        {!notebook[0].isUploading &&
                <button>
                <a href={`https://ned-web-app.herokuapp.com/downloads/${filename}`}>Download</a>
              </button>
              }
      </div>
    </div>
  )
}

export default Notebook