import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSpinner, faX } from '@fortawesome/free-solid-svg-icons'
import './FileItem.scss'

const FileItem = ({ file, deleteFile }) => {
    return (
        <div>
        <div className='file'>
            <li
                className="file-item"
                key={file.name}>
                <a href={`https://ned-web-app.herokuapp.com//downloads/${file.name}`}>{file.name}</a>
                <div className="actions">
                    <div className="loading"></div>
                    {file.isUploading && <FontAwesomeIcon
                        icon={faSpinner} className="fa-spin"
                        onClick={() => deleteFile(file.name)} />
                    }
                    {!file.isUploading &&
                        <FontAwesomeIcon icon={faX}
                            onClick={() => deleteFile(file.name)} />
                    }
                </div>
            </li>
            </div>
        </div>
    )
}

export default FileItem