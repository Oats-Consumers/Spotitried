# Local Database Setup

1. Install PostgreSQL 14+
2. Create user + database:

   psql -U postgres -c "CREATE USER oats_consumers WITH PASSWORD 'oats_consumed';"
   psql -U postgres -c "CREATE DATABASE spotitried;"
   psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE spotitried TO oats_consumers;"

3. Run schema + seed scripts:

   psql -U oats_consumers -d spotitried -f db/scripts/schema.sql
   psql -U oats_consumers -d spotitried -f db/scripts/seed_data.sql

4. Connect using:

   - Host: localhost
   - Port: 5432
   - User: oats_consumers
   - Password: oats_consumed
   - Database: spotitried
