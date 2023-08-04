export default async function fetchMusicRecommendations(){

    const settings = {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        
    }
    
    const response = await fetch('http://localhost:3001/fetch_recommendations', settings);
    const data = await response.json();

    return data
}
