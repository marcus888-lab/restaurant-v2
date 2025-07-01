#!/bin/bash

echo "🚀 Starting Coffee Shop Database..."

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Start the database
docker-compose up -d postgres

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 3

# Check if database is running
if docker-compose ps | grep -q "coffee_shop_db.*Up"; then
    echo "✅ Database is running successfully!"
    echo "📊 Connection string: postgresql://coffee_admin:coffee_secret_2024@localhost:5432/coffee_shop"
    echo ""
    echo "To view logs: docker-compose logs -f postgres"
    echo "To stop database: ./scripts/db-stop.sh"
else
    echo "❌ Failed to start database. Check logs with: docker-compose logs postgres"
    exit 1
fi