export default async function startMusicES(){

    const settings = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        
    }
    
    const response = await fetch('http://localhost:3001/execute_es', settings);
    const data = await response.json();

    return data
}
