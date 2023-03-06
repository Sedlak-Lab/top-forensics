import React, {useState} from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus } from '@fortawesome/free-solid-svg-icons'
import './FileUpload.scss'
import axios from 'axios'
import FileItem from "../FileItem/FileItem"
import Alert from 'react-bootstrap/Alert';

const FileUpload = ({ files, setFiles, removeFile }) => {
    const [show, setShow] = useState(false)

    async function uploadHandler(event) {
        const file = event.target.files[0];
        event.target.value = "";
        console.log(file)
        if(!file) return;
        file.isUploading = true;
        setFiles([file])

        const formData = new FormData();
        formData.append(
            "newFile",
            file,
            file.name
        )
        console.log(formData)
        await axios.post('https://top-forensics.herokuapp.com/upload', formData)
            .then((res) => {
                if (res.status === 202) {
                    console.log("Wrong Format")
                    setShow(true)
                    file.isUploading = false;
                    deleteFileHandler(file.name)
                } else {
                    file.isUploading = false;
                    setFiles([file])
                }
            })
            .catch((err) => {
                console.error(err)
                removeFile(file.name)
            });
            console.log(formData)
        }

    async function deleteFileHandler(_name) {
        await axios.delete(`https://top-forensics.herokuapp.com/upload/${_name}`)
        .then((res) => removeFile(_name))
        .catch((err) => console.error(err));
    }


    return (
        <div>
            <div className="file-card">
                <div className="file-inputs">
                    <input type="file" onChange={uploadHandler} />
                    <button>
                        <i>
                            <FontAwesomeIcon icon={faPlus} />
                        </i>
                        Upload
                    </button>
                </div>
                <p className="input"><a href={"https://top-forensics.herokuapp.com/uploads/upload_template.csv"}>Download Template File</a></p>
                {
                        show && 
                              <Alert variant="danger" onClose={() => setShow(false)} dismissible bsPrefix='alert'>
                                <Alert.Heading>Wrong Format!</Alert.Heading>
                                <p>
                                  Please download the template and upload in molar units again.
                                </p>
                              </Alert>
                    }
                <ul className="file-list">
                    {
                        files &&
                        files.map(f => (<FileItem
                            key={f.name}
                            file={f}
                            deleteFile={deleteFileHandler} /> ))
                    }
                </ul>
            </div>
        </div>
    )
}

export default FileUpload