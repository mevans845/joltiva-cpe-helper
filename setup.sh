#!/usr/bin/env bash

echo "setting up the environment file"
touch .env
echo "VERSION=1.0.0" >> .env
echo "Creating Logs folder"
mkdir logs