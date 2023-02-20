import React, {useState} from 'react'
import './App.scss';
import FileUpload from './Components/FileUpload/FileUpload';
import Container from 'react-bootstrap/Container'
import Nav from 'react-bootstrap/Nav'
import Navbar from 'react-bootstrap/Navbar'
import Notebook from './Components/Notebook/Notebook'
import axios from 'axios'
import InitialBook from './Components/Notebook/Initialbook';

function App() {

  const [files, setFiles] = useState([])
  console.log(files)
  
  const removeFile = (filename) => {
    setFiles(files.filter((file => file.name !== filename)))
  }


  return (
    <div>
    <Navbar bg="light" variant='light'>
      <Container>
        <Navbar.Brand href='#home'>PFAS Forensics Using the TOP Assay</Navbar.Brand>
        <Nav className="me-auto">
          <Nav.Link href="#home">Home</Nav.Link>
        </Nav>
      </Container>
    </Navbar>
    <div className='view'>
      <div className="App">
          <FileUpload files={files} setFiles = {setFiles} removeFile={removeFile} />
        </div>
        <div className='Notebook'>
          {Array.isArray(files) && files.length ? <Notebook notebook={files} /> : <InitialBook />}
        </div>
    </div>
    </div>
  );
}

export default App;
