# Simple Sample Scheduler

## Requirements
- Python >= 3.4
- Django 1.10.1

## Usage

Get new sample:
```
curl -g -i -X GET http://localhost:8000/scheduler/small_sample_queue/ -H "X-IP: $ip"
```

Finish with sample:
```
curl -g -i -X POST http://localhost:8000/scheduler/small_sample_completed/ -H "X-IP: $ip" -H "X-UUID: $uuid"
```