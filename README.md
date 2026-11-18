# Database Migrations with Alembic

### 1. Install Alembic
```bash
uv add alembic
```

### 2. Initialize Migrations Folder
Run once to set up the migration environment:
```bash
uv run alembic init migrations
```

### 3. One-Time Setup Configuration
Before generating migrations:
- In `alembic.ini`, set your database URL:
  ```ini
  sqlalchemy.url = sqlite:///./test.db
  ```
- In `app/db.py`, configure a `naming_convention` on `Base.metadata` (required for SQLite batch mode to prevent unnamed constraint errors):
  ```python
  from sqlalchemy import MetaData
  from sqlalchemy.orm import DeclarativeBase

  naming_convention = {
      "ix": "ix_%(column_0_label)s",
      "uq": "uq_%(table_name)s_%(column_0_name)s",
      "ck": "ck_%(table_name)s_%(constraint_name)s",
      "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
      "pk": "pk_%(table_name)s",
  }

  class Base(DeclarativeBase):
      metadata = MetaData(naming_convention=naming_convention)
  ```
- In `migrations/env.py`, connect your models' metadata and enable batch mode for SQLite:
  ```python
  from app.db import Base
  target_metadata = Base.metadata

  # In both run_migrations_offline() and run_migrations_online(), add:
  render_as_batch=True
  ```

### 4. Generate a Migration
Run whenever you make changes to your SQLAlchemy models:
```bash
uv run alembic revision --autogenerate -m "describe changes here"
```

### 5. Apply Migrations
Apply pending migrations to update the database schema:
```bash
uv run alembic upgrade head
```

### 6. Helpful Migration Commands
- **Check current applied revision:**
  ```bash
  uv run alembic current
  ```
- **View migration history:**
  ```bash
  uv run alembic history
  ```
- **Rollback the last migration:**
  ```bash
  uv run alembic downgrade -1
  ```
