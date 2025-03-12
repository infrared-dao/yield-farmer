#!/bin/bash

while true; do
    poetry run python -m src.yield_farmer >> logs/yield_farmer_cron.log 2>&1
    sleep 7200  # 2 hours
done