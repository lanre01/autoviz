import React from 'react';
import { useLocation } from 'react-router-dom';

function Processed(prop) {

    const location = useLocation();
    const { result } = location.state || {};

    /* const [img, setImage] = useState(); */

    return (
        <div>
            <h1>Result</h1>
            {result ? (
                <div>{result}</div>
            ) : (
                <p>No result found. Please upload a file first.</p>
            )}
        </div>
    );
}

export default Processed;