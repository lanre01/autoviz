import classes from './NavBar.module.css'

function NavBar() {
    return (
        <div className={classes.navbar}>
            <div className={classes.text}>
                Automatic Visualisation
            </div>
            <div className={classes.about}>
                <a href='#'>About</a>
            </div>
        </div>
    )
}

export default NavBar;



