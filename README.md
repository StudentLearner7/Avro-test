
# Name of the HTML file
html_file="api_results.html"

# Clear the HTML file or create a new one
echo "" > "$html_file"

# Define colors
red="<span style=\"color: red;\">"
green="<span style=\"color: green;\">"
blue="<span style=\"color: blue;\">"
end_span="</span>"

# Get start time
start_time=$(date "+%Y-%m-%d %H:%M:%S")

# Define an array of API endpoints with names
declare -a api_endpoints=(
    "API 1|https://api.example.com/endpoint1"
    "API 2|https://api.example.com/endpoint2"
    # Add more API endpoints here in the format "Name|Endpoint"
)

# Loop through the API endpoints
for endpoint_info in "${api_endpoints[@]}"
do
    IFS="|" read -ra api_info <<< "$endpoint_info"
    api_name="${api_info[0]}"
    api_endpoint="${api_info[1]}"

    api_response=$(curl -s -w "\n%{http_code}" "$api_endpoint")

    status_code=$(echo "$api_response" | tail -n 1)
    response_body=$(echo "$api_response" | sed '$d')

    # Only capture responses with non-200 status codes
    if [ "$status_code" != "200" ]; then
        echo "<h2>$red API Name: $api_name $end_span</h2>" >> "$html_file"
        echo "<p>Endpoint: $blue <a href=\"$api_endpoint\">$api_endpoint</a> $end_span</p>" >> "$html_file"
        echo "<p>Status Code: $red $status_code $end_span</p>" >> "$html_file"
        echo "<pre>$response_body</pre>" >> "$html_file"
        echo "<hr>" >> "$html_file"

        echo "$api_name - Non-200 response captured."
    else
        echo "<h2>$green API Name: $api_name $end_span</h2>" >> "$html_file"
        echo "<p>Endpoint: $blue <a href=\"$api_endpoint\">$api_endpoint</a> $end_span</p>" >> "$html_file"
        echo "<p>Status Code: $green $status_code $end_span</p>" >> "$html_file"
        echo "<hr>" >> "$html_file"

        echo "$api_name - 200 OK response."
    fi
done

# Get end time
end_time=$(date "+%Y-%m-%d %H:%M:%S")

# Add start and end time to the HTML file
echo "<h2>Start Time: $start_time</h2>" >> "$html_file"
echo "<h2>End Time: $end_time</h2>" >> "$html_file"

echo "API testing completed. Results are stored in $html_file."