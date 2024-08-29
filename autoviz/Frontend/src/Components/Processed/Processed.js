import React from 'react';
import { useLocation } from 'react-router-dom';

function Processed(prop) {

    const location = useLocation();
    const data = location.state?.data;
    

    /* const [img, setImage] = useState(); */

    return (
        <div>
            <h1>Result</h1>
            {data ? (
                <div>{data.filename}</div>
            ) : (
                <p>No result found. Please upload a file first.</p>
            )}
        </div>
    );
}

export default Processed;