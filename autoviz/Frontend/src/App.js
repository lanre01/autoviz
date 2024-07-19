import React, { Component } from 'react';
import {BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import './App.css';
import Footer from './Components/Footer/Footer'
import NavBar from './Components/NavBar/Navbar';

import Processed from './Components/Processed/Processed';
import Home from './Components/Home/Home';


function App() {


    let routes = (
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/processed' element={<Processed/>}/>
      </Routes>
    )

    return(
      <Router>
        <div className="App">
          <NavBar></NavBar>
          <main>
            {routes}
          </main>
          <Footer />
        </div>
      </Router>
      
    )

}

export default App;
