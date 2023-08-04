import React from "react";
import "./styles.css";
import { Message, ChatFeed } from "./react-chat-ui";
import Form from "./form";
import getPrompt from "./getMusicPrompt.js"
import { useState, useEffect } from "react";
import Card_layout from "./Card_layout";
import Card_layout_music from "./Card_layout_music";

import ResultsPageSongs from "./resultsPageSongs";
const styles = {
  button: {
    backgroundColor: "#fff",
    borderColor: "#1D2129",
    borderStyle: "solid",
    borderRadius: 20,
    borderWidth: 2,
    color: "#1D2129",
    fontSize: 18,
    fontWeight: "300",
    paddingTop: 8,
    paddingBottom: 8,
    paddingLeft: 16,
    paddingRight: 16,
    outline: "none"
  },
  selected: {
    color: "#fff",
    backgroundColor: "#0084FF",
    borderColor: "#0084FF"
  }
};

const users = {
  0: "You",
  1: "Nella"
};

class Chat extends React.Component {
  constructor() {

    super();
    this.musicEsStarter = require('./startMusicES').default;
    this.introIntent = require('./getIntroIntent').default;

    this.fetchMusicRecs = require('./fetchMusicRecommendations').default;
    this.fetchHousingRecs = require('./fetchHousingRecommendations').default;
    
    this.getHousingPrompt = require('./getHousingPrompt').default;
    this.getMusicPrompt = require('./getMusicPrompt').default;
   
    this.mode = "";
    
    this.introInput = {"message": String};
    this.input = {"message": String};
    
    this.state = {
      messages: [
        new Message({ id: "0", message: " '1' for spotify \n'2' for housing", senderName: "Nella" }),
        
      ],
      useCustomBubble: false,
      curr_user: 0,
      mode: 'neither'
    };

    this.chatState = true;
    this.resultsState = false;
    this.recommendations = [];
    this.introPromptFlag = true;
    this.prompt_number = 0;
    this.housingMode = false;
    this.musicMode = false;
    
    this.musicEsStarter().then(
      ()=>console.log("ES-Music Started"));
      

  }

    add_prompt(data){
      //add prompt to chatfeed
      this.state.curr_user = 2
      const prevState = this.state;

      const newMessage = new Message({
      id: this.state.curr_user,
      message: data,
      senderName: "Nella",
    
    });
    prevState.messages.push(newMessage);
    this.setState(this.state);


    }

    fetchPrompt(input=null){
      //this.respond_housing()

      if (this.housingMode){
        this.getHousingPrompt(input).then(data => {
          console.log(data + "!!!!!!!!!");
          this.add_prompt(data);
        })
      }
      if (this.musicMode)
      this.getMusicPrompt(input).then(data => {
        this.add_prompt(data["prompt"]);
      });


      
    }


    onPress(user) {
      this.setState({ curr_user: user });
    }

    pushSong(song){
      this.state.curr_user = 2
      const prevState = this.state;
      const newMessage = new Message({
        id: this.state.curr_user,
        message: song,
        senderName: "You",
      
      });
      prevState.messages.push(newMessage);
      this.setState(this.state);
    }

    sendAnswer(){
      if (this.musicMode){
        this.fetchMusicRecs()
        .then(data => { 
          console.log(data)
          this.recommendations = data;
          console.log(this.recommendations)
        })
      }
      if(this.housingMode){
        this.fetchHousingRecs()
        .then(data => { 
          console.log(data)
          this.recommendations = data;
        })
      }
    }

    setpromptType(input){

        if(input == "housing"){
          this.housingMode = true;

        }
        if(input == "music"){
          this.musicMode = true
        }

        
    }

    


    //Called on form submit in form.js
    pushMessage(recipient, message) {
      
      //add to chat feed
      this.state.curr_user = 0;

      const prevState = this.state;

      const newMessage = new Message({
        id: this.state.curr_user,
        message,
        senderName: "You",
      });

      prevState.messages.push(newMessage);
      this.setState(this.state);
      this.input.message = message;

      //return message to backend
      this.prompt_number = this.prompt_number + 1;
      if(this.introPromptFlag != false){
        
        //this.sendAnswer()
        this.introPromptFlag = false;
        
        
      // this.introIntent(this.input)
      //   .then(data => (
      //     this.mode = data
         
          
      //   ))
        
      //   console.log(this.mode);

      if(message == "1"){
        this.musicMode = true
      }
      if(message == "2"){
        this.housingMode = true
      }


      } else{
        if(this.prompt_number > 1){
          this.sendAnswer();
        }
      }
      
      this.fetchPrompt(this.input);
      
      

    }

    

    render() {

      if (this.housingMode){
        return (
          <div class="parent"> 
          
            <div className="container">
            <Card_layout recs= {this.recommendations}>
              
              </Card_layout>
            </div>
         
            <div className="container">
        
                <div className="chatfeed-wrapper">
                  <ChatFeed
                    chatBubble={this.state.useCustomBubble}
                    messages={this.state.messages} // Boolean: list of message objects
                    showSenderName
                  />
                </div>
                <div>
                  <Form chat = {this}></Form>
                </div>
              </div>
            </div>   
                
              );
      }

      else{
        return (
          <div class="parent"> 
          
            <div className="container">
            <Card_layout_music recs= {this.recommendations}>
              
              </Card_layout_music>
            </div>
         
            <div className="container">
        
                <div className="chatfeed-wrapper">
                  <ChatFeed
                    chatBubble={this.state.useCustomBubble}
                    messages={this.state.messages} // Boolean: list of message objects
                    showSenderName
                  />
                </div>
                <div>
                  <Form chat = {this}></Form>
                </div>
              </div>
            </div>   
                
              );
      }

     

      
    }
}

export default Chat;
