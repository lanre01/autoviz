import { useState } from "react";

function Dropdown({ textHead, initialStyle, children}) {
    const [display, setDisplay] = useState(initialStyle);

    const toggleDropdown = () => {
        setDisplay(display === 'none' ? 'block': 'none');
    };

    return (
        <div>
            <div onClick={toggleDropdown}>{textHead}</div>
            <div style={{display}}>{children}</div>
        </div>
    );
}

export default Dropdown;