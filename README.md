# Project Name

Brief description of the project.

## How to run

### Option 1: Local Setup

#### OSX:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### Windows:
```
python3 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

### Option 2: Docker

1. Build the Docker image:
```
docker build -t dd .
```

2. Run the Docker container:
```
docker run -p 8000:8000 dd
```

## WebSocket Example Client

In (multiple) browsers, navigate to http://localhost:8000/static/client.html

## Contributing

For information on contributing to this project, please see the [CONTRIBUTE.md](CONTRIBUTE.md) file.
