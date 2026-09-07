#!/bin/sh

APP_DIR="/opt/agent"

echo "Install WireGuard Agent"


mkdir -p $APP_DIR/logs


chmod +x $APP_DIR/wg_agent.py


echo "Agent installed"

echo "Config:"
echo "$APP_DIR/config.json"
