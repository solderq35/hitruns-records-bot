#!/bin/bash

# Check if main.py is already running
if ps aux | grep -v grep | grep "main.py" > /dev/null
then
    echo "main.py is already running, skipping restart."
else
    # If not running, start main.py
    python main.py &
    echo "main.py started."
fi

# Start cron.py regardless
python cron.py &
echo "cron.py started."
