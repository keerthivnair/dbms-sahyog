import React from 'react';
import './App.css';
import Header from './components/Header';
import Navbar from './components/Navbar';
import Banner from './components/Banner';
import Footer from './components/Footer';
import About from './components/About'; // Import the About component
import Register from './components/Register'; // Import the Register component
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Import routing
import "slick-carousel/slick/slick.css"; 
import "slick-carousel/slick/slick-theme.css"; 
import VolunteerForm from './components/VolunteerForm';

function App() {
 return (
   <Router>
     <div className="App">
       <Header/>
       <Navbar/>
       <Routes>
         {/* Default Route - Landing page with Banner */}
         <Route path="/" element={<Banner />} />
         {/* About Page Route */}
         <Route path="/about" element={<About />} />
         {/* Register Page Route */}
         <Route path="/register" element={<Register />} />
         <Route path="/volunteer" element={<VolunteerForm/>} />
       </Routes>
    
       <Footer />
     </div>
   </Router>
 );
}

export default App;
