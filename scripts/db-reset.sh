#!/bin/bash

echo "⚠️  WARNING: This will DELETE ALL DATABASE DATA!"
echo "Are you sure you want to reset the database? (yes/no)"
read -r response

if [ "$response" != "yes" ]; then
    echo "❌ Operation cancelled."
    exit 0
fi

echo "🔄 Resetting Coffee Shop Database..."

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed."
    exit 1
fi

# Stop and remove containers and volumes
docker-compose down -v

# Start fresh database
echo "🚀 Starting fresh database..."
docker-compose up -d postgres

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 5

# Check if database is running
if docker-compose ps | grep -q "coffee_shop_db.*Up"; then
    echo "✅ Database reset successfully!"
    echo "📊 Fresh database is now running"
    echo ""
    echo "Next steps:"
    echo "1. Run database migrations"
    echo "2. Seed initial data if needed"
else
    echo "❌ Failed to start fresh database. Check logs with: docker-compose logs postgres"
    exit 1
fi