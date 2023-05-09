#!/bin/bash

DIRECTORY="backend/app/data"

# Making the entrypoint script executable
echo "Setting execute permissions for backend/entrypoint.sh"
chmod +x backend/entrypoint.sh



if [ ! -d "$DIRECTORY" ]; then
  echo "Directory does not exist. Creating..."
  mkdir -p "$DIRECTORY"
else
  echo "Directory already exists."
fi


# Running the Python script to prepare the database data
echo "Running the Python script to prepare the database data"
python backend/prepare_db_data.py
if [ $? -ne 0 ]; then
    echo "Failed to run the Python script, exiting" >&2
    exit 1
fi

echo "Script completed successfully"
