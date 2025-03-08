#!/bin/bash

# Website URL for Silver prices
URL="https://tradingeconomics.com/commodity/silver"

# Fetch the HTML content
HTML=$(curl -s "$URL")

# Extract the Silver price using regex
SILVER_PRICE=$(echo "$HTML" | grep -oP '(?<="value":)[0-9.]+' | head -1)

# Get current timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Output file
OUTPUT_FILE="silver_prices.csv"

# If file doesn't exist, create it with a header
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Timestamp,Price" > "$OUTPUT_FILE"
fi

# Append the data
echo "$TIMESTAMP,$SILVER_PRICE" >> "$OUTPUT_FILE"

echo "Scraped Silver Price: $SILVER_PRICE USD (Saved to $OUTPUT_FILE)"
