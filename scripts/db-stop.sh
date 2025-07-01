#!/bin/bash

echo "🛑 Stopping Coffee Shop Database..."

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed."
    exit 1
fi

# Stop the database
docker-compose stop postgres

echo "✅ Database stopped successfully!"