import React, {useState} from 'react'
import './Notebook.scss'
import Spinner from 'react-bootstrap/Spinner';

const Notebook = ({notebook}) => {
  const filename = notebook[0].name
  console.log(filename)
  const [load, setLoad] = useState(false)


  return (
    <div className='render'>
      <div className='notebook'>
        <img src={`https://top-forensics.herokuapp.com/render/${filename}?${Date.now()}`} alt="Notebook" onLoad={() => setLoad(true)}/>
        {!notebook[0].isUploading && load === true ?
                <button>
                <a href={`https://top-forensics.herokuapp.com/downloads/${filename}`}>Download</a>
              </button> : <div style={{ height: "500px", marginLeft : "500px"}} className="justify-content-center align-items-center">
        <Spinner
          animation="border"
          role="status"
          style={{ width: "4rem", height: "4rem" }}
        ></Spinner>
        </div>
              }
      </div>
    </div>
  )
}

export default Notebook