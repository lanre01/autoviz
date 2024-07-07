import React, { useState } from 'react';

function FileExplorer() {
    
    const [selectedFile, setSelectedFile] = useState();
    const [fileTitle, setFileTitle] = useState();

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setFileTitle(file.name);
        setSelectedFile(file);

        if (file) {
        // You can use FileReader here to read the file content
        const reader = new FileReader();
        reader.onload = (e) => {
            const fileContent = e.target.result;
            console.log(fileContent); // Process the file content as needed
        };
        reader.readAsText(file); // Read the file as text
        
        }
    };

    const sendFile = () => {
        // send the file to the the backend.
    }
    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onSubmit={sendFile}>Submit</button>
        </div>
    );
}

export default FileExplorer;