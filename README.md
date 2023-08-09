const fs = require('fs');

function generateReport(apiCalls) {
    const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>API Test Report</title>
        </head>
        <body>
            <h1>API Test Report</h1>
            <table>
                <tr>
                    <th>API Name</th>
                    <th>Endpoint</th>
                    <th>Status Code</th>
                    <th>Response</th>
                </tr>
                ${generateRows(apiCalls)}
            </table>
        </body>
        </html>
    `;

    fs.writeFileSync('api_report.html', htmlContent);
}

function generateRows(apiCalls) {
    return apiCalls
        .map(call => `
            <tr>
                <td>${call.name}</td>
                <td>${call.endpoint}</td>
                <td>${call.statusCode}</td>
                <td>${call.statusCode !== 200 ? call.response : ''}</td>
            </tr>
        `)
        .join('');
}

module.exports = generateReport;