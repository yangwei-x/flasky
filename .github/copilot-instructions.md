# Project Guidelines

## Code Style
- Follow the existing Flask and SQLAlchemy patterns in `app/main/views.py`, `app/api/posts.py`, and `app/models.py` instead of introducing new abstractions for small changes.
- Keep blueprint-local code in its package: UI routes, forms, and errors live under `app/main/` or `app/auth/`; API handlers and auth helpers live under `app/api/`.
- Match the existing test style in `tests/`: this project uses `unittest` test cases with `create_app('testing')`, an explicit app context, and per-test `db.create_all()` / `db.drop_all()` isolation.

## Architecture
- The app uses the application factory pattern. Create and configure apps through `create_app(config_name)` in `app/__init__.py`; the Flask CLI entry point is `flasky.py`.
- Registered blueprints are `main` for server-rendered pages, `auth` under `/auth`, and `api` under `/api/v1`.
- Extensions are initialized in `app/__init__.py`; database models and most business rules live in `app/models.py`; schema migrations live in `migrations/versions/`.
- Reuse the existing permission and role helpers (`permission_required`, `admin_required`, `Permission`, `Role`) instead of duplicating authorization checks in views.

## Build And Test
- Install development dependencies with `make dev`. To sync an existing virtualenv to a lock file, use `make sync FILE=requirements/dev.txt`.
- Run the full test suite with `make test`. Run coverage with `make test-cov`. For a focused run, use `python -m flask test tests/test_user_model.py`.
- Prefer the existing Flask CLI test command over `pytest` so test runs match the repository's current setup.
- If you change dependencies, edit the relevant `requirements/*.in` files and regenerate the matching lock files with `make lock` or `make lock-all`.

## Conventions
- `flasky.py` loads a root `.env` file automatically. Keep configuration changes compatible with the `FLASK_CONFIG`, `DATABASE_URL`, `DEV_DATABASE_URL`, and `TEST_DATABASE_URL` environment variables used in `config.py`.
- Testing uses the `testing` config, which disables CSRF and defaults to an in-memory SQLite database. Preserve that behavior when adding tests.
- After changing models, add or update an Alembic migration in `migrations/versions/` and verify the app can apply it with Flask-Migrate.
- API endpoints should follow the existing JSON patterns: validate permissions through the API decorators, serialize with the model `to_json()` helpers, and return resource URLs from the `api` blueprint.

See `README.md` for the full dependency lock workflow, database setup, and environment-specific install options.