#!/bin/bash
set -e

# Fix permissions
chown -R waterpark:waterpark /vol/static /vol/media
chmod -R 775 /vol/static /vol/media

# Execute command
exec gosu waterpark "$@"
