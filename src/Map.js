import React from "react";
import "./table_style.css";
import {GoogleMap, useLoadScript, MarkerF} from "@react-google-maps/api";
import { useState, useEffect } from "react";

function Map(cord) {

    console.log(cord.cord );
    console.log(cord.cord.lat);
    console.log(cord.cord.lng);


    const {isLoaded} = useLoadScript({ googleMapsApiKey: "AIzaSyDZw9fgJrpYhET7vXGG36a9nrBY6cQp7HA"});

    if(!isLoaded) return <div>Loading...</div>
    return(
    
      <GoogleMap 
            zoom= {5.5} 
            center={{lat: cord.cord.lat, lng: cord.cord.lng}} 
            mapContainerClassName='map-container'>

            
                
                <MarkerF
                position={{lat: cord.cord.lat, lng: cord.cord.lng}}
                
                
                />
            
            
        </GoogleMap>
    
    )
    
}

export default Map;