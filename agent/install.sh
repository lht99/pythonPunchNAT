#!/bin/sh

echo "Install NAS Gateway Agent"


BASE="$(cd "$(dirname "$0")" && pwd)"


mkdir -p "$BASE/logs"


chmod +x "$BASE/nas_agent.py"


echo "Agent installed"
echo "Location:"
echo "$BASE"
