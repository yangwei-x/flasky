Flasky
======

This repository contains the source code examples for the second edition of my O'Reilly book [Flask Web Development](http://www.flaskbook.com).

The commits and tags in this repository were carefully created to match the sequence in which concepts are presented in the book. Please read the section titled "How to Work with the Example Code" in the book's preface for instructions.

For Readers of the First Edition of the Book
--------------------------------------------

The code examples for the first edition of the book were moved to a different repository: [https://github.com/miguelgrinberg/flasky-first-edition](https://github.com/miguelgrinberg/flasky-first-edition).

Dependency Management
-----------------------------

This fork now adopts a pip-tools based workflow.

Layered files:

1. `*.in` (e.g. `requirements/base.in`, `dev.in`, `docker.in`, `heroku.in`, `prod.in`) list direct dependencies (unpinned, may include `-r base.in`).
2. `*.txt` are generated lock files (exact versions + provenance comments) via `pip-compile` and are what you install from.

Common commands:

Generate / refresh all locks:

Option 1 (script):
```
./scripts/update_locks.sh            # all
./scripts/update_locks.sh dev        # only dev
U=1 ./scripts/update_locks.sh base   # upgrade base deps
UPKG=Flask,SQLAlchemy ./scripts/update_locks.sh base dev
HASHES=1 ./scripts/update_locks.sh   # include hashes
```

Option 2 (Makefile):
```
make lock-all
make lock TARGETS="base dev"
U=1 make lock TARGETS="base"
```

Install (dev):
```
pip install -r requirements/dev.txt
```

Install (production):
```
pip install -r requirements/prod.txt
```

Install (Heroku / docker images respectively):
```
pip install -r requirements/heroku.txt
pip install -r requirements/docker.txt
```

Exact env sync (will uninstall anything not in the files):
```
pip install pip-tools
pip-sync requirements/prod.txt      # or dev.txt etc.
# OR via Makefile
make sync FILE=requirements/dev.txt
```

Upgrade strategies (via script / Makefile):

* All packages (base): `U=1 ./scripts/update_locks.sh base` (or `U=1 make lock TARGETS="base"`)
* Single package upgrade (example Flask): `UPKG=Flask ./scripts/update_locks.sh base`
* Multiple specific packages: `UPKG=Flask,SQLAlchemy ./scripts/update_locks.sh base`
* Add hashes for stronger supply‑chain guarantees: `HASHES=1 ./scripts/update_locks.sh` (combine flags, e.g. `U=1 HASHES=1 ./scripts/update_locks.sh base`)

Direct `pip-compile` commands remain possible if you prefer manual control; the script simply wraps them with sensible defaults.

Recommended workflow:

1. Edit a `*.in` (add/remove direct deps).
2. Re-run selective `pip-compile` (only affected stacks) or the full batch.
3. Run tests, lint, security scan.
4. Commit changed `*.in` + corresponding `*.txt` together.

Legacy `constraints*.txt` snapshots have been superseded by the generated `*.txt` lock files.

Database Setup
--------------

This Flask application supports both MySQL and PostgreSQL databases.

### Supported Databases

#### MySQL
- **Python Library**: `mysqlclient`
- **Connection String**: `mysql://username:password@host:port/database`
- **Docker Service**: Available in `docker-compose.yml`

#### PostgreSQL
- **Python Library**: `psycopg2-binary`
- **Connection String**: `postgresql://username:password@host:port/database`
- **Alternative Format**: `postgres://username:password@host:port/database`

### Configuration

#### Environment Variables
Set the `DATABASE_URL` in your `.env` file:

```bash
# MySQL example
DATABASE_URL=mysql://flasky:password@localhost:3306/flasky

# PostgreSQL example
DATABASE_URL=postgresql://flasky:password@localhost:5432/flasky
```

### Local Development Setup

#### MySQL
```bash
# Install MySQL server
sudo apt-get install mysql-server

# Create database and user
mysql -u root -p
CREATE DATABASE flasky;
CREATE USER 'flasky'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON flasky.* TO 'flasky'@'localhost';
FLUSH PRIVILEGES;
```

For production/remote access:
```sql
CREATE SCHEMA `flasky` DEFAULT CHARACTER SET utf8mb4;
CREATE USER 'flasky'@'%' IDENTIFIED BY 'flasky.2025';
GRANT ALL PRIVILEGES ON flasky . * TO 'flasky'@'%';
```

#### PostgreSQL
```bash
# Install PostgreSQL server
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE flasky;
CREATE USER flasky WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE flasky TO flasky;
```

For production setup:
```sql
CREATE USER flasky WITH PASSWORD 'flasky.2025';
CREATE DATABASE flasky OWNER flasky;
GRANT ALL PRIVILEGES ON DATABASE flasky TO flasky;
```

Connect to PostgreSQL:
```bash
psql -h 127.0.0.1 -U flasky
```

### Docker Setup
Use the provided `docker-compose.yml` which includes MySQL service:

```bash
docker-compose up -d
```

For PostgreSQL with Docker, modify `docker-compose.yml` to use postgres image instead of mysql.

### Database Migration

After setting up your database:

```bash
# Initialize migration repository (first time only)
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### Testing

The application includes database tests. Run them with:

```bash
python -m pytest tests/
```

### Production Considerations

- **MySQL**: Use `mysqlclient` for better performance in production
- **PostgreSQL**: Use `psycopg2` (compiled) instead of `psycopg2-binary` for production
- **Connection Pooling**: Consider using connection pooling for high-traffic applications
- **SSL**: Enable SSL connections in production environments