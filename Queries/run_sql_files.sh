#!/bin/bash

# Database connection details
# DB_NAME = "tpc" (no index) OR "tpc_citus_index"
DB_NAME="tpc"

# You can find <current user> value by running "SELECT current_user;" in PostgreSQL shell 
DB_USER="victoriagao"

DB_HOST="localhost"
DB_PORT="5432"

# File containing the list of SQL files
# "no_index_queries.txt" or "index_queries.txt"
SQL_FILE_LIST="no_index_queries.txt"

# Directory to store output files
# OUTPUT_DIR = "results_no_index_trialX" or "results_index_trialX" where X is trial # (i.e., 1, 2, 3)
OUTPUT_DIR="results_no_index_trial4"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Read each file from the list
while IFS= read -r file
do
    echo "Processing file: $file"

    # Get the base name of the SQL file without the extension
    base_name=$(basename "$file" .sql)

    # Define the output file name
    output_file="$OUTPUT_DIR/${base_name}_output.txt"

    # Run the SQL file and save the output
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$file" > "$output_file" 2>&1

    echo "Output saved to: $output_file"
done < "$SQL_FILE_LIST"
