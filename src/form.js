import React, { useState } from 'react';
import "./styles.css";

export default function Form({ chat}) {
    const [name, setName] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    chat.pushMessage("1", name);
    
    var allInputs = document.querySelectorAll('input');
    allInputs.forEach(singleInput => singleInput.value = '');
    
  }


  

  return (
    <form onSubmit={handleSubmit}>
        <div class="input-group">
          <input
            id="myForm" 
            class = "form-control"
            type="text" 
            value={name}
            onChange={(e) => setName(e.target.value)}
            
            placeholder="Type a message..."
            
          />

          <button class="button-9" role="button">Submit</button>
          </div>
          
        
      
      
    </form>
  );
}