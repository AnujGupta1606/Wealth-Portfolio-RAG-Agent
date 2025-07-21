#!/bin/bash

# Install dependencies
npm install

# Add serve package for serving static files
npm install -g serve

# Build the React app
npm run build

echo "Frontend build completed successfully!"
