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
import CampForm from './components/Campform';
import VolunteerDetails from './components/VolunteerDetails';
import Login from './components/Login';
import VolunteerLogin from './components/Volunteerlogin';
import CampLogin from './components/Camplogin';
import UpdateCamp from './components/UpdateCamp';
import CampOptions from './components/CampOptions';
import NGORegistration from './components/NgoRegistration';

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
         <Route path="/login" element={<Login />} />
         <Route path="/volunteer" element={<VolunteerForm/>} />
         <Route path="/camp" element={<CampForm/>} />
         <Route path="/ngo" element={<NGORegistration/>} />
         <Route path="/volunteer-login" element={<VolunteerLogin/>} />
         <Route path="/volunteer-details" element={<VolunteerDetails/>} />
         <Route path="/camp-login" element={<CampLogin/>} />
         <Route path="/camp-options" element={<CampOptions />} />
         <Route path="/update-camp" element={<UpdateCamp />} />
        
       </Routes>
    
       <Footer />
     </div>
   </Router>
 );
}

export default App;
