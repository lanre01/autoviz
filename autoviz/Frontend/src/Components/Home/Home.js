import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import axios from 'axios';
import classes from './Home.module.css'

function Home() {
    
    const [_file, setFile] = useState();
    const navigate = useNavigate();

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];

        if(selectedFile && selectedFile.name.endsWith('.csv') && selectedFile.type === 'text/csv') {
            setFile(event.target.files[0]);
        }
        else {
            setFile(null)
            alert('Please upload a valid csv file');
        }
        
    };

    const sendFile = async (event) => {
        event.preventDefault();
        
        if (!_file) {
            alert('No valid file selected.');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', _file); 
    
        try {
            const response = await axios.post('/api/compute', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.log(response.data);
            // push the response data to the processed page
            navigate('/Processed', { state: {data: response.data} });
        
    
        } catch(error) {
            console.error('Error uploading file: ', error);
        }
    }
    return (
        <div className={classes.home}>
            <form onSubmit={sendFile}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Upload</button>
            </form>
        </div>
    );
}

export default Home;