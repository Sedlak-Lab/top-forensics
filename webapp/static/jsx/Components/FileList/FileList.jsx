import React from 'react'
import axios from 'axios'
import FileItem from "./../FileItem/FileItem"

const FileList = ({ files, removeFile}) => {
    async function deleteFileHandler(_name) {
        await axios.delete(`https://ned-web-app.herokuapp.com/upload?name=${_name}`)
        .then((res) => removeFile(_name))
        .catch((err) => console.error(err));
    }
  return (
    <ul className="file-list">
        {
            files &&
            files.map(f => (<FileItem
                key={f.name}
                file={f}
                deleteFile={deleteFileHandler} /> ))
        }
    </ul>
  )
}

export default FileList;