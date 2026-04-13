#!/bin/bash
set -e

# Generate config.toml from environment variables
python - <<'EOF'
import toml, os

hosts_env = os.environ.get('FRONT_HOSTS', 'http://localhost,http://127.0.0.1')
hosts = [h.strip() for h in hosts_env.split(',')]

config = {
    'db_connection': {
        'db_name': os.environ.get('DB_NAME', 'three-row-game'),
        'db_user': os.environ.get('DB_USER', 'postgres'),
        'db_password': os.environ.get('DB_PASSWORD', 'user'),
        'db_host': os.environ.get('DB_HOST', 'localhost'),
        'db_port': int(os.environ.get('DB_PORT', '5432')),
    },
    'front_connection': {
        'hosts': hosts
    }
}

with open('config.toml', 'w') as f:
    toml.dump(config, f)

print('config.toml generated with db_host =', config['db_connection']['db_host'])
EOF

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
