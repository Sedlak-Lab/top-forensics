import React, {useState} from 'react'
import './Notebook.scss'

const Notebook = ({notebook}) => {
  const filename = notebook[0].name
  console.log(filename)
  const [load, setLoad] = useState(false)


  return (
    <div className='render'>
      <div className='notebook'>
        <img src={`https://ned-web-app.herokuapp.com/render/${filename}?${Date.now()}`} alt="Notebook" onLoad={() => setLoad(true)}/>
        {!notebook[0].isUploading && load === true ?
                <button>
                <a href={`https://ned-web-app.herokuapp.com/downloads/${filename}`}>Download</a>
              </button> : <div></div>
              }
      </div>
    </div>
  )
}

export default Notebook