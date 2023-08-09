import http from 'k6/http';
import { sleep } from 'k6';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';

export let options = {
    thresholds: {
        // Define your performance thresholds here if needed
    },
    // Output an HTML report after the test completes
    ext: {
        loadimpact: {
            projectID: 123456, // Replace with your LoadImpact project ID if you have one
            name: 'Functional Test',
        },
    },
};

export default function () {
    let apiEndpoints = [
        'https://api.example.com/api1',
        'https://api.example.com/api2',
        // ... add more API endpoints here
    ];

    let responses = [];

    for (let endpoint of apiEndpoints) {
        let response = http.get(endpoint);
        responses.push({ endpoint, body: response.body });
    }

    // Simulate some wait time
    sleep(5); // Sleep for 5 seconds

    // Create an HTML report with the API responses
    let htmlContent = `
        <html>
            <head>
                <title>API Responses</title>
            </head>
            <body>
                <h1>API Responses</h1>
                <ul>
                    ${responses.map(res => `<li><strong>${res.endpoint}</strong>: ${res.body}</li>`).join('')}
                </ul>
            </body>
        </html>
    `;

    // Save the HTML content to a file
    let reportFile = open('api_responses.html', 'w');
    reportFile.write(htmlContent);
    reportFile.close();
}