import classes from './Footer.module.css'

function Footer() {

    return (
        <div className={classes.footer}>
            <div>
                <p>About</p>
                <p>
                    This is part of the 2023/2024 academic year module at the University of Nottingham.
                </p>
            </div>
            <div>
                <p>Contributors</p>
                <ul>
                    <li>Lawal Alongbija</li>
                    <li>Kito Theoron</li>
                    <li>Samiul</li>
                    <li>James</li>
                    <li>Oliver Butcher</li>
                </ul>
            </div>
        </div>
    )
}

export default Footer;