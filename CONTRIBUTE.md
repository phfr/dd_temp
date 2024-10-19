# Contributing to Project Name

Thank you for your interest in contributing to our project! This document provides guidelines and information for contributors.

## Development Setup

1. Clone the repository:

   TODO: Add correct link to repo

   ```
   git clone https://github.com/username/project-name.git
   cd project-name
   ```

2. Create and activate a virtual environment:

   ### OSX/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   ### Windows:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

## Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to run tests and enforce commit message formatting with [commitizen](https://commitizen-tools.github.io/commitizen/) before commits. To set up the hooks:

### OSX/Linux:
```bash
bash setup_hooks.sh
```

### Windows:
```bash
setup_hooks.bat
```

## Running Tests

To run the test suite:
```
pytest
```

## Code Structure

The project is structured as follows:

1. **Main Application**
   - `app.py`: The main entry point of the application.

2. **Server Components**
   - `server_components.py`: Contains functions for creating and configuring the FastAPI app.

3. **WebSocket Management**
   - `utils/websocket_manager.py`: Manages WebSocket connections, events, and client information.

4. **Event Handlers**
   - `handlers/`: Directory containing individual event handler modules.

5. **API Routes**
   - `routes/`: Directory containing API route definitions.

6. **Utility Modules**
   - `utils/API_framework.py`: Abstracts web framework specifics.
   - `utils/custom_logging.py`: Configures logging for the application.

7. **Static Files**
   - `static/`: Directory for static files, including `client.html`.

8. **Tests**
   - `tests/`: Directory containing test files.

9. **Docker Configuration**
   - `Dockerfile`: Defines the Docker image for the application.

10. **Dependencies**
    - `requirements.txt`: Lists the Python package dependencies for the main application.
    - `requirements-dev.txt`: Lists additional dependencies for development and testing.

## Submitting Changes

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them using Commitizen standards (see below)
4. Push your changes to your fork
5. Submit a pull request to the main repository

### Using Commitizen for Commits

This project uses Commitizen to standardize commit messages. To create a commit:

1. Stage your changes:
   ```
   git add .
   ```

2. Instead of using `git commit`, use:
   ```
   cz commit
   ```

3. Follow the prompts to create a standardized commit message. This will typically include:
   - Type of change (feat, fix, docs, style, refactor, test, chore)
   - Scope of the change (optional)
   - Short description
   - Longer description (optional)
   - Breaking changes (if any)
   - Issues closed (if any)

Example of a commit message created with Commitizen:

```
feat(auth): add user authentication system

- Implement JWT token-based authentication
- Add login and logout endpoints
- Create user model and database migrations

BREAKING CHANGE: API now requires authentication for most endpoints
```

Using Commitizen ensures that all commit messages follow a consistent format, which helps with generating changelogs and understanding the project history.

## Questions?

If you have any questions or need further clarification, please open an issue or contact the maintainers.
