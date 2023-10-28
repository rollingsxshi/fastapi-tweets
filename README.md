# FastAPI tweet

A simple CRUD api where users can create, read, update & delete a tweet.
Also comes with admin features to get all tweets & delete any tweet.
Users route to get current user & change password

Uses
- sqlalchemy as orm
- alembic for data migrations
- passlib[bcrypt] to hash passwords
- python-jose for jwt
- supabase for postgres db
- python-dotenv to read .env file locally

## JWT
- used for dealing with *authorization*
- `poetry add "python-jose[cryptography]"`
- `openssl rand -hex 32` to generate secret key

## Alembic
- db migration tool with sqlalchemy
- `poetry add alembic`
- `alembic init <folder name>`: init new, generic env
- `alembic revision -m <message>`: create new revision of env
- `alembic upgrade <revision #>`: run upgrade migration to db
- `alembic downgrade -1`: run downgrade migration to db
- run `alembic init alembic` to create alembic directory
- run `alembic revision --autogenerate -m "generate initial migration"`
- run `alembic upgrade head` to add tables to db