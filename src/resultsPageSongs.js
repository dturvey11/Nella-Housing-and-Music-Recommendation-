import React from "react";
import "./table_style.css";
import {GoogleMap, useLoadScript, MarkerF} from "@react-google-maps/api";
import { useState, useEffect } from "react";

function ResultsPageSongs (recs) {



  const {isLoaded} = useLoadScript({ googleMapsApiKey: "AIzaSyDZw9fgJrpYhET7vXGG36a9nrBY6cQp7HA"});
 
  console.log("&&&&&&&&&&&");
  console.log(recs)
  const [accessToken, setAccessToken] = useState("");

  const [final_Tracks, setFinal_Tracks] = useState("");

  var recommendations = recs.recs;
  
  var locations = [
    [33.13, -117.07],
    [37.31, -121.94],
    [33.95, -118.02],
    [34.09, -118.21],
    [35.27, -118.83],
    [33.86, -118.33],
    [32.85, -115.57],
    [34.07, -118.27],
    [34.12, -118.08],
    [37.77, -122.27],
    [34.28, -118.89],
    [36.79, -120.08],
  ];

  if(recs.recs.length == 0) return <div class="table-wrapper"><p>No Recommendations</p></div>
  if(!isLoaded) return <div>Loading...</div>
  console.log("-----------------------------------")
  console.log(recommendations);
  return(
    
    
    <div class="table-wrapper">
      <h3>
        Check out Nellas Recommendations
      </h3>
    <table class="fl-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Artist</th>
            <th>Album</th>
            <th>Genre</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          
          {
            recommendations.map( song => 
              <tr>
              <td>{song.name}</td>
              <td>{song.artist}</td>
              <td>{song.album}</td>
              <td>N/A</td>
              <td>
                <a href={song.url} target="_blank">{song.url} </a>
                
              </td>
            </tr>
            )
          }
          
          
        </tbody>
      </table>

    <div>
      <GoogleMap 
        zoom= {6} 
        center={{lat:37, lng:-120}} 
        mapContainerClassName='map-container'>

          {locations.map(subarray => 
            
            <MarkerF
              position={{lat: subarray[0], lng: subarray[1]}}
              key= {subarray[0]}
              
            />,
          
          )}
        </GoogleMap>
      </div>
    </div>
    
  )
}




export default ResultsPageSongs;