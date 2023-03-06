import React, {useState} from 'react'
import './App.scss';
import FileUpload from './Components/FileUpload/FileUpload';
import Container from 'react-bootstrap/Container'
import Nav from 'react-bootstrap/Nav'
import Navbar from 'react-bootstrap/Navbar'
import Notebook from './Components/Notebook/Notebook'
import axios from 'axios'
import InitialBook from './Components/Notebook/Initialbook';
import Alert from 'react-bootstrap/Alert';

function App() {

  const [files, setFiles] = useState([])
  const [showAbout, setshowAbout] = useState(false)
  console.log(files)
  const file = files[0]
  
  const removeFile = (filename) => {
    setFiles([])
  }


  return (
    <div>
    <Navbar bg="light" variant='light'>
      <Container className='mx-15 my-10'>
        <Navbar.Brand href='#home'>PFAS Forensics Using the TOP Assay</Navbar.Brand>
        <Nav className="me-auto">
          <Nav.Link href="#home">Home</Nav.Link>
          <Nav.Link href="#home" onClick={() => setshowAbout(true)}>About</Nav.Link>
        </Nav>
      </Container>
    </Navbar>
    <div className='view'>
      <div className="App">
          <FileUpload files={files} setFiles = {setFiles} removeFile={removeFile} />
        </div>
        {
                        showAbout ?
                              <Alert variant="light" onClose={() => setshowAbout(false)} dismissible bsPrefix='alert'>
                                <Alert.Heading>About</Alert.Heading>
                                <p>
                                This research was funded by the Strategic Environmental Research and Development Program (SERDP ER-1330). 
                                If you have questions or would like to contribute TOP data, please email David Sedlak at sedlak@berkeley.edu.
                                 The web app was developed by Jacob T. Kim in collaboration with Edmund Antell and David Sedlak. 
                                 For complete documentation, visit our GitHub page at <a href="https://github.com/Sedlak-Lab/top-forensics">https://github.com/Sedlak-Lab/top-forensics</a>.
                                </p>
                              </Alert> :
                              <div className='Notebook'>
          {Array.isArray(files) && files.length && !file.isUploading ? <Notebook notebook={files} /> : <InitialBook />}
        </div>
          }
    </div>
    </div>
  );
}

export default App;
