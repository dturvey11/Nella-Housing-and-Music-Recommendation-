export default async function getIntroIntent(input){

    const settings = {
        method: 'POST',
        headers: {
            
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Methods':'POST,PATCH,OPTIONS'
            
        },
        body: JSON.stringify(input)
    }


    const response = await fetch('http://localhost:8090/classify_intent', settings);
    const data = await response.json();
    
    return data
}