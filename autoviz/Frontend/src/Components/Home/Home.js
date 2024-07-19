import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';
import classes from './Home.module.css'

function Home() {
    
    const [file, setFile] = useState();
    const history = useHistory();

    const [fileTitle, setFileTitle] = useState();

    const handleFileChange = (event) => {
        const _file = event.target.files[0];
        setFileTitle(_file.name);
        setFile(_file);

        /* if (file) {
        // You can use FileReader here to read the file content
        const reader = new FileReader();
        reader.onload = (e) => {
            const fileContent = e.target.result;
            console.log(fileContent); // Process the file content as needed
        };
        reader.readAsText(file); // Read the file as text
        
        } */
    };

    const sendFile = async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://server:5000/compute', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            // push the response data to the processed page
            history.push('/processed', {result: response.data});

        } catch(error) {
            console.error('Error uploading file:', error);
        }
    }
    return (
        <div className={classes.home}>
            <form onSubmit={sendFile}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Upload</button>
            </form>
            <input type="file" onChange={handleFileChange} />
            <button onSubmit={sendFile}>Submit</button>
        </div>
    );
}

export default Home;