import React from "react";
import './carousel.css'
import {GoogleMap, useLoadScript, MarkerF} from "@react-google-maps/api";
import {useEffect, useState} from "react";
import  Map  from "./Map";

function Card_layout_music(recs) {
    
var data = recs.recs;
console.log(data);


var music = false
var housing = false
const {isLoaded} = useLoadScript({ googleMapsApiKey: "AIzaSyDZw9fgJrpYhET7vXGG36a9nrBY6cQp7HA"});

const images = importAll(require.context('./data/houses_dataset', false, /\.(png|jpe?g|svg)$/));


          useEffect(() => {
            if(recs.recs.length != 0){
            const buttons = document.querySelectorAll("[data-carousel-button]")
    
            buttons.forEach(button => {
              button.addEventListener("click", () => {
                const offset = button.dataset.carouselButton === "next" ? 1 : -1
                const slides = button
                  .closest("[data-carousel]")
                  .querySelector("[data-slides]")
          
                const activeSlide = slides.querySelector("[data-active]")
                let newIndex = [...slides.children].indexOf(activeSlide) + offset
                if (newIndex < 0) newIndex = slides.children.length - 1
                if (newIndex >= slides.children.length) newIndex = 0
          
                slides.children[newIndex].dataset.active = true
                 delete activeSlide.dataset.active
              })
            })
          }
          })
          console.log(recs)
      if(recs.hasOwnProperty() == {}){
        console.log("##########{}");
      }
      if(recs.recs[0] == undefined){
        
        return(
          <section aria-label="Newest Photos">
        <div >
          <h1>Welcome To Nella </h1>
          
          <h3>A recommendation system for housing AND music </h3>
          
          <h3>You can even talk to Nella like a real person!</h3>
          
          <h3>First select a system to interact with, housing or music!</h3>
          
          <h3>Answer Nella's prompts and get real time recommendations</h3>
          

          
          </div>
          </section>
        )}
      //re-init data to an array it comes in as weird object
        var d = [];
        for(var i in data){
          d.push(data[i]);
        }
        data = d;
        

        data.map((item) => {
          console.log(item);
        });
        
      return(
        <section aria-label="Newest Photos">
        <div class="carousel" data-carousel>
          <button class="carousel-button prev" data-carousel-button="prev">&#8656;</button>
          <button class="carousel-button next" data-carousel-button="next">&#8658;</button>
          <ul data-slides>
          <li class="slide" data-active>
              <div class="center-screen">
              <h1>
                  
                  Use the arrows to scroll through Tracks
                  <br></br>
                </h1>
              </div>
              


          
            </li>
            {
              data.map(item =>(
                
                <li class="slide">
              <img src={item.cover_url} alt="Nature Image #1"></img>
              <div>
                <h2>
                  
                  {item.name}
                  
                </h2>
                <h3 class = "black-text">
                  {"Artist: " + item.artist}
                  <br></br>
                  {"Album: " + item.album}
                  <br></br>
                  
                  <a href={item.url}> Spotify Link</a>
                  
                  
                </h3>
                
          </div>
            </li>
              ))
              
            }
            
            
          </ul>
        </div>
        
      </section>
  
      )



                         
        //             data.map((item) => (
                    
                    
                        
        //                 <div>
        //                     <h1>
                                
        //                         {"Price: $" + item.price.toLocaleString("en-US")}
        //                         <br></br>
        //                     </h1>
        //                     <h2>
        //                         {"Area: " + item.area}
        //                         <br></br>
        //                         {"Bathrooms: " + item.bathrooms}
        //                         <br></br>
        //                         {"Berdooms:" + item.bedrooms}
        //                         <br></br>
        //                         {"Flooring: " + item.house_flooring}
        //                         <br></br>
        //                         {"Age: " + item.house_age}
        //                         <br></br>
        //                         {"Nearby Transport: " + item.house_public_transport}
        //                         <br></br>
        //                         {"Coordinates: " + item.latitude + ", " + item.longitude}
        //                         <br></br>
        //                         {"Neighborhood_features: " + item.neighborhood_features}
        //                         <br></br>
        //                         {"School Rating: " + item.schools_rating}
        //                         <br></br>
        //                         {"Sea Proximity: " + item.sea_proximity}
        //                     </h2>
        //                 </div>
        
        //             ))
        //         }

}

function importAll(r) {
  let images = {};
  r.keys().map((item, index) => { images[item.replace('./', '')] = r(item); });
  return images;
}





export default Card_layout_music;