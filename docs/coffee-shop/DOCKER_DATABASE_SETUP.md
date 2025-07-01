# Docker Compose Database Setup

## 📋 Prerequisites

- Docker installed on your machine
- Docker Compose installed
- Basic understanding of Docker concepts

## 🐳 Docker Compose Configuration

Create a `docker-compose.yml` file in your project root:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: coffee_shop_db
    restart: unless-stopped
    environment:
      POSTGRES_USER: coffee_admin
      POSTGRES_PASSWORD: coffee_secret_2024
      POSTGRES_DB: coffee_shop
    ports:
      - "5432:5432"
    volumes:
      - coffee_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U coffee_admin -d coffee_shop"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  coffee_data:
    name: coffee_shop_postgres_data
```

## 🚀 Quick Start

### 1. Start the Database
```bash
# Start PostgreSQL in detached mode
docker-compose up -d postgres

# Check if the container is running
docker-compose ps

# View logs
docker-compose logs -f postgres
```

### 2. Stop the Database
```bash
# Stop the container
docker-compose stop postgres

# Stop and remove the container
docker-compose down

# Stop and remove container + volumes (WARNING: This deletes all data)
docker-compose down -v
```

## 🔧 Database Connection

### Connection String
```
postgresql://coffee_admin:coffee_secret_2024@localhost:5432/coffee_shop
```

### Environment Variables
Create a `.env` file for your application:
```env
DATABASE_URL=postgresql://coffee_admin:coffee_secret_2024@localhost:5432/coffee_shop
```

### Python Connection Example
```python
import asyncpg

async def connect():
    conn = await asyncpg.connect(
        host='localhost',
        port=5432,
        user='coffee_admin',
        password='coffee_secret_2024',
        database='coffee_shop'
    )
    return conn
```

### Prisma Configuration
In your `schema.prisma`:
```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

## 📊 Database Management

### Access PostgreSQL CLI
```bash
# Connect to the database using psql
docker-compose exec postgres psql -U coffee_admin -d coffee_shop

# Run SQL commands
\dt                    # List all tables
\d+ table_name        # Describe table structure
\q                    # Quit psql
```

### Backup Database
```bash
# Create a backup
docker-compose exec postgres pg_dump -U coffee_admin coffee_shop > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
docker-compose exec -T postgres psql -U coffee_admin coffee_shop < backup_20240101_120000.sql
```

## 🛡️ Security Best Practices

1. **Change Default Credentials**: Always use strong passwords in production
2. **Use Secrets**: Store passwords in Docker secrets or environment files
3. **Network Isolation**: Consider using custom Docker networks
4. **Regular Backups**: Set up automated backup procedures

### Production-Ready Configuration
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: coffee_shop_db
    restart: always
    environment:
      POSTGRES_USER_FILE: /run/secrets/postgres_user
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
      POSTGRES_DB: coffee_shop
    ports:
      - "127.0.0.1:5432:5432"  # Only bind to localhost
    volumes:
      - coffee_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d  # Initial SQL scripts
    networks:
      - coffee_network
    secrets:
      - postgres_user
      - postgres_password

networks:
  coffee_network:
    driver: bridge

secrets:
  postgres_user:
    file: ./secrets/postgres_user.txt
  postgres_password:
    file: ./secrets/postgres_password.txt

volumes:
  coffee_data:
    name: coffee_shop_postgres_data
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 5432
   lsof -i :5432
   
   # Use a different port in docker-compose.yml
   ports:
     - "5433:5432"
   ```

2. **Permission Denied**
   ```bash
   # Fix volume permissions
   sudo chown -R 999:999 /var/lib/docker/volumes/coffee_shop_postgres_data
   ```

3. **Container Won't Start**
   ```bash
   # Check logs for errors
   docker-compose logs postgres
   
   # Remove and recreate
   docker-compose rm -f postgres
   docker-compose up -d postgres
   ```

## 📚 Additional Resources

- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🎯 Next Steps

1. Set up database migrations with Prisma
2. Configure database monitoring
3. Implement automated backups
4. Set up development vs production configurations