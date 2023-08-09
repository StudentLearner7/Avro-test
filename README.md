import http from 'k6/http';
import { writeFileSync } from 'k6/fs';

const endpoints = [
  'https://endpoint1.com',
  'https://endpoint2.com',
  // ... add all 10 endpoints
];

let html = '<table><tr><th>Endpoint</th><th>Status Code</th><th>Response</th></tr>';

export default function () {
  endpoints.forEach(endpoint => {
    let res = http.get(endpoint);
    let truncatedResponse = res.body.length > 200 ? res.body.substring(0, 200) : res.body;
    html += `<tr><td>${endpoint}</td><td>${res.status}</td><td>${truncatedResponse}</td></tr>`;
  });
}

export function handleSummary(data) {
  html += '</table>';
  return {
    'report.html': html,
  };
}

export let options = {
  iterations: 1,
};
