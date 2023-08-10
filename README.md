const responseJson = JSON.parse(responseBody);

// Recursive function to check status
const checkStatusRecursive = (json) => {
    for (const key in json) {
        if (typeof json[key] === 'object') {
            checkStatusRecursive(json[key]);
        } else if (key === 'status' && json[key] !== 'UP') {
            pm.test('Status is not UP', false);
            return;
        }
    }
};

// Start checking status
for (const key in responseJson) {
    if (typeof responseJson[key] === 'object') {
        checkStatusRecursive(responseJson[key]);
    }
}