import classes from './Footer.module.css'
import Dropdown from '../Util/Dropdown';



function Footer() {

    return (
        <div className={classes.footer}>
            <div>
                <h3>About</h3>
                <p>
                    This is part of the 2023/2024 academic year module at the University of Nottingham.
                </p>
            </div>
            <div>
                <h4>Contributors</h4>
                {/* Add emails and linkedln links to each name using icons */}
                <ul>
                    <li>
                        Lawal Alongbija
                    </li>
                    <li>
                        Kito Theoron
                    </li>
                    <li>
                        Saniul
                    </li>
                    <li>
                        James
                    </li>
                    <li>
                        Oliver Butcher
                    </li>
                    <li>
                        Yash Awashi
                    </li>
                    <li>
                        Tom
                    </li>
                </ul>
            </div>
        </div>
    )
}

export default Footer;