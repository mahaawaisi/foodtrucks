import React, { useState } from "react";
import axios from 'axios';


const LocationForm = ({ onSubmit }) => {
  const [location, setLocation] = useState("");
  const [radius, setRadius] = useState("");

  const handleGetLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
       async (position) => {
          setLocation(`${position.coords.latitude},${position.coords.longitude}`);
          try{
            const response = await axios.get("http://localhost:5000/data", {params:{lat: position.coords.latitude, long:position.coords.longitude}});
          }catch(error){
            console.error("Error fetching food trucks: ", error);
          }
        },
        (error) => {
          console.error("Error getting user location:", error);
        }
      );
    } else {
      console.error("Geolocation is not supported by this browser");
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ location, radius });
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Location:
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
      </label>
      <label>
        Radius (miles):
        <input
          type="number"
          value={radius}
          onChange={(e) => setRadius(e.target.value)}
        />
      </label>
      <button type="submit">Find Food Trucks</button>
      <button type="button" onClick={handleGetLocation}>
      Use my current location
      </button>
    </form>
    
  );
};

export default LocationForm;
