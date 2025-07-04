#!/bin/bash
# Find the PID using port 11434 and kill it
PID=$(lsof -ti tcp:11434)
if [ -z "$PID" ]; then
  echo "No process found using port 11434."
  exit 1
fi
echo "Stopping process with PID $PID using port 11434..."
kill -9 $PID 