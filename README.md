#!/bin/bash

# Name of the HTML file
html_file="api_results.html"

# Clear the HTML file or create a new one
echo "" > "$html_file"

# Define an array of API endpoints
api_endpoints=(
    "https://api.example.com/endpoint1"
    "https://api.example.com/endpoint2"
    # Add more API endpoints here
)

# Loop through the API endpoints
for ((i=0; i<${#api_endpoints[@]}; i++))
do
    api_response=$(curl -s "${api_endpoints[$i]}")

    # Append the API response to the HTML file
    echo "<h2>API Call $((i+1))</h2>" >> "$html_file"
    echo "<pre>$api_response</pre>" >> "$html_file"
    echo "<hr>" >> "$html_file"

    echo "API Call $((i+1)) done."
done

echo "All API calls completed. Results are stored in $html_file."