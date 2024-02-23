import React, { useState } from "react";
import axios from 'axios';
import './App.css'

const LocationForm = ({ onSubmit }) => {
  const [latitude, setLat] = useState("");
  const [longitude, setLon] = useState("");
  const [truckData, setTruckData] = useState(null);
  const [buttonClicked, setButtonClicked] = useState(false);

  const handleGetLocation = async (useCurrentLocation) => {
    setTruckData(null);
    setButtonClicked(true);

    if (useCurrentLocation) {
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {
          const { latitude, longitude } = position.coords;
          axios.get('http://localhost:5000/data', {
            params: {
              lat: latitude,
              lon: longitude
            }
          })
          .then((response) => {
            if (Array.isArray(response.data)) {
              // Transform data so we can display
              const transformedData = response.data.map(truck => ({
                id: truck.locationid,
                name: truck.name,
                address: truck.address,
                menu: truck.menu,
                status: truck.status,
                x_coordinate: truck.X,
                y_coordinate: truck.Y,
                latitude: truck.Latitude,
                longitude: truck.Longitude,
                coordinates: truck.Location,
                distance: truck.distance,
              }));
              setTruckData(transformedData);
            } else {
              console.error("Invalid truck data:", response.data);
            }
          })
          .catch((error) => {
            console.error("Error getting food truck data: ", error);
          });
        });
      } else {
        alert("Location permissions are not enabled by your browser.");
      }
    } else {
      const lat = latitude;
      const lon = longitude;
      axios.get('http://localhost:5000/data', {
        params: {
          lat: lat,
          lon: lon
        }
      })
      .then((response) => {
        // Handle response
        if (Array.isArray(response.data)) {
          const transformedData = response.data.map(truck => ({
            id: truck.locationid,
            name: truck.name,
            address: truck.address,
            menu: truck.menu,
            status: truck.status,
            x_coordinate: truck.X,
            y_coordinate: truck.Y,
            latitude: truck.Latitude,
            longitude: truck.Longitude,
            coordinates: truck.Location,
            distance: truck.distance,
          }));
          setTruckData(transformedData);
          console.log(transformedData);
        } else {
          console.error("Invalid truck data:", response.data);
        }
      })
      .catch((error) => {
        console.error("Error getting food truck data: ", error);
      });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleGetLocation(false); 
  };

  return (
  <div className="container">
    <h1 className="heading">Let's search for food trucks near you!</h1>
    <div className="button-container">
      <button type="button" onClick={() => handleGetLocation(true)}>Use current location</button>
      <span className="button-text">OR</span>
      <form onSubmit={handleSubmit}>
        <label>
          Latitude:
          <input
            type="text"
            value={latitude}
            onChange={(e) => setLat(e.target.value)}
          />
        </label>
        <label>
          Longitude:
          <input
            type="text"
            value={longitude}
            onChange={(e) => setLon(e.target.value)}
          />
        </label>
        <button type="submit">
          Use coordinates
      </button>
      </form>
    </div>
      {(buttonClicked && truckData && truckData.length > 0 ) && (
        <div>
          <h2>Food Trucks Near You</h2>
          <ul>
            {truckData.map((truck, index) => (
              <div key={index}>
                <p><strong>{truck.name}</strong></p>
                <p><strong>Address:</strong> {truck.address}</p>
                <p><strong>Menu:</strong> {truck.menu}</p>
                <p><strong>Distance from you:</strong> {truck.distance.toFixed(2)} km away</p>
              </div>
            ))}
          </ul>
        </div>
      )}
      {buttonClicked && truckData && truckData.length === 0 && (
        <p>No food trucks near you.</p>
      )}
    </div>
  );
};

export default LocationForm;
