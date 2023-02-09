#!/bin/sh

set -e

echo "$(date '+%F %T.%3N %Z')" "[flask] INFO: running start.sh"

env=${FLASK_DEBUG:-1}

if [ "$env" = "production" ]; then
  echo "$(date '+%F %T.%3N %Z')" "[flask] INFO: running production environment"
  gunicorn --bind 0.0.0.0:5000 --timeout 120 --chdir ./ms ms:app
elif [ "$env" = 'testing' ]; then
  echo "$(date '+%F %T.%3N %Z')" "[flask] INFO: running testing environment"
  coverage run -m pytest
  coverage report
else
  echo "$(date '+%F %T.%3N %Z')" "[flask] INFO: running development environment"
  flask run --host=0.0.0.0
fi
