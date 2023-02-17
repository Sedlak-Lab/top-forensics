import React from 'react'
import './Notebook.scss'

const Notebook = ({notebook}) => {
  const filename = notebook[0].name
  console.log(filename)


  return (
    <div className='render'>
      <div className='notebook'>
        {/* <img src={ {image} } alt="Notebook" /> */}
        <img src={`http://127.0.0.1:5000/render/${filename}`} alt="Notebook" />
        {!notebook[0].isUploading &&
                <button>
                <a href={`http://127.0.0.1:5000/downloads/${filename}`}>Download</a>
              </button>
              }
      </div>
      {/* <div className="download">
        <button>
          Download
        </button>
      </div> */}
    </div>
  )
}

export default Notebook