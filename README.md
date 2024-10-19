# DataDiVR-backend

DataDiVR-backend is the server-side component of the DataDiVR project, designed to handle data processing and communication for the DataDiVR visualization system.

## Features

- WebSocket server for real-time communication
- Data processing and analysis capabilities
- Supports multiple concurrent client connections

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation and Running

#### Option 1: Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/DataDiVR-backend.git
   cd DataDiVR-backend
   ```

2. Set up a virtual environment and install dependencies:

   **OSX / Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   **Windows:**

   ```powershell
   python3 -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory and add your configuration:

     ```text
     LOG_LEVEL=DEBUG
     ```

   - Alternatively, set environment variables in your shell or use the provided run scripts.

4. Run the application:
   - debug: `LOG_LEVEL=DEBUG python app.py`
   - less log output: `LOG_LEVEL=INFO python app.py`
   - (same as: `python app.py`)

#### Option 2: Docker

1. Build the Docker image:

   ```bash
   docker build -t datadivr-backend .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 8000:8000 datadivr-backend
   ```

The server will be available at `http://localhost:8000`.

## Testing the WebSocket Connection

To test the WebSocket connection, open `http://localhost:8000/static/client.html` in multiple browser windows. This client example demonstrates real-time communication with the server.

## Contributing

Please refer to the [CONTRIBUTE.md](CONTRIBUTE.md) file for detailed information on:

- Project structure
- Coding standards
- Submission guidelines
- Development workflow

## License

[Specify the license here, e.g., MIT, Apache 2.0, etc.]

## Contact

[Provide contact information or links to project maintainers/community]
