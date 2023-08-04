export default async function fetchHousingRecommendations(input){

    const settings = {
        method: 'GET',
        headers: {
            
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(input)
    }
    
    const response = await fetch('http://localhost:8090/fetch_recommendations', settings);
    const data = await response.json();

    return data
}
