export default function () {
  console.log('\x1b[36m%s\x1b[0m', 'Endpoint\tStatus Code\tResponse');
  
  endpoints.forEach(endpoint => {
    let res = http.get(endpoint);
    let truncatedResponse = res.body.length > 200 ? res.body.substring(0, 200) : res.body;

    console.log('\x1b[32m%s\x1b[0m', `${endpoint}\t${res.status}\t${truncatedResponse}`);
  });
}