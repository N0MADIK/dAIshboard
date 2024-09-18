// component/NavBar.js

import { NavLink } from "react-router-dom";

const NavBar = () => {
    console.log("HERE!")
    return (
        <nav>
            <ul>
                <li>
                    <NavLink to="/projects">Projects</NavLink>
                </li>
            </ul>
        </nav>
    );
};

export default NavBar;