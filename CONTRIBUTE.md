# Contributing to DataDiVR-backend


## Table of Contents

- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Code Structure](#code-structure)
- [Submitting Changes](#submitting-changes)
- [Using Commitizen for Commits](#using-commitizen-for-commits)
- [Code Style, Linting, and VSCode Setup](#code-style-linting-and-vscode-setup)

## Development Setup

1. Clone the repository:

   TODO: Add correct link to repo

   ```bash
   git clone https://github.com/username/project-name.git
   cd project-name
   ```

2. Create and activate a virtual environment:

   ### OSX/Linux

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   ### Windows

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install development dependencies

   ```bash
   pip install -r requirements-dev.txt
   ```

   This will install all the necessary dependencies for development, including testing and linting tools.

4. Pre-commit Hooks

   This project uses [pre-commit](https://pre-commit.com/) to run tests, linting, and formatting checks before commits. The configuration for pre-commit is in the `.pre-commit-config.yaml` file. To set up the hooks:

   #### Setup for OSX/Linux

   ```bash
   bash setup_hooks.sh
   ```

   #### Setup for Windows

   ```powershell
   .\setup_hooks.bat
   ```

## Development Tools

This project uses several development tools to ensure code quality and consistency:

1. **pytest**: For running the test suite.
2. **black**: For code formatting.
3. **flake8**: For linting.
4. **isort**: For sorting imports.
5. **pre-commit**: For running checks before commits.
6. **commitizen**: For standardizing commit messages.

These tools and their versions are specified in the `requirements-dev.txt` file. The pre-commit hooks are configured in the `.pre-commit-config.yaml` file to run automatically before each commit.

## Code Structure

The project is structured as follows:

1. **Main Application**
   - `app.py`: The main entry point of the DataDiVR-backend application.

2. **Server Components**
   - `server_components.py`: Contains functions for creating and configuring the DataDiVR-backend, including static file serving, event handlers, route handlers, and WebSocket endpoints.

3. **WebSocket Management**
   - `utils/websocket/`: Directory containing WebSocket-related modules:
     - `__init__.py`: Initializes and exports the WebSocketManager instance.
     - `websocket_manager.py`: Integrates various components for managing WebSocket connections, events, and client information.
     - `client_manager.py`: Manages client connections and information.
     - `event_handler.py`: Handles WebSocket events and their execution.
     - `event_decorator.py`: Provides a decorator for registering event handlers.
     - `broadcaster.py`: Handles broadcasting messages to clients.

4. **Event Handlers**
   - `handlers/`: Directory containing individual event handler modules (e.g., welcome, hello, ping, long_task).

5. **API Routes**
   - `routes/`: Directory containing API route definitions (e.g., sum).

6. **Utility Modules**
   - `utils/`: Directory containing utility modules:
     - `API_framework.py`: Abstracts web framework specifics.
     - `custom_logging.py`: Configures logging for the application.
     - `names.py`: Manages unique name generation for clients.

7. **Static Files**
   - `static/`: Directory for static files, including `client.html` for WebSocket testing.

8. **Tests**
   - `tests/`: Directory containing test files for various components.

9. **Configuration Files**
   - `.pre-commit-config.yaml`: Configuration for pre-commit hooks.
   - `pyproject.toml`: Configuration for tools like Commitizen.
   - `pytest.ini`: Configuration for pytest.
   - `.vscode/`: Directory containing VSCode-specific settings and extension recommendations.

10. **Docker Configuration**
    - `Dockerfile`: Defines the Docker image for the application.

11. **Dependencies**
    - `requirements.txt`: Lists the Python package dependencies for the main application.
    - `requirements-dev.txt`: Lists additional dependencies for development and testing.

12. **Documentation**
    - `README.md`: Provides an overview of the project and setup instructions.
    - `CONTRIBUTE.md`: Guidelines for contributing to the project.

13. **Setup Scripts**
    - `setup_hooks.sh`: Bash script for setting up pre-commit hooks on Unix-like systems.
    - `setup_hooks.bat`: Batch script for setting up pre-commit hooks on Windows.

## Submitting Changes

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them using Commitizen standards (see below)
4. Push your changes to your fork
5. Submit a pull request to the main repository

### Using Commitizen for Commits

This project enforces standardized commit messages using [Commitizen](https://commitizen-tools.github.io/commitizen/). Standardized commit messages help with generating changelogs and understanding the project history. You can learn more about the benefits of standardized commit messages in this [article about conventional commits](https://www.conventionalcommits.org/).

While you can use the normal `git commit` (or whatever UI) command if you're familiar with the required format, we recommend using the interactive Commitizen command, especially if you're unsure about the formatting. Here's how to create a commit:

1. Stage your changes

   ```bash
   git add .
   ```

2. To use the interactive Commitizen command (recommended for those unfamiliar with the format)

   ```bash
   cz commit
   ```

   Follow the prompts to create a standardized commit message. This will typically include:
   - Type of change (feat, fix, docs, style, refactor, test, chore)
   - Scope of the change (optional)
   - Short description
   - Longer description (optional)
   - Breaking changes (if any)
   - Issues closed (if any)

3. If you're familiar with the Commitizen format, you can use the standard git commit command

   ```bash
   git commit -m "type(scope): short description"
   ```

   Make sure your commit message follows the Commitizen format to pass the pre-commit hooks.

   Example of a commit message created with Commitizen:

   ```text
   feat(auth): add user authentication system

   - Implement JWT token-based authentication
   - Add login and logout endpoints
   - Create user model and database migrations

   BREAKING CHANGE: API now requires authentication for most endpoints
   ```

## Code Style, Linting, and VSCode Setup

This project follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for code style and docstrings. Please refer to this guide when writing code and documentation for the project.

This project uses several tools for code formatting and linting:

1. **Black**: For code formatting
2. **Flake8**: For linting
3. **isort**: For import sorting
4. **Pre-commit**: To run checks before commits

To set up your VSCode environment:

1. Install the recommended VSCode extensions:
   VSCode will automatically suggest installing the recommended extensions when you open the project.

2. VSCode Settings:
   The project includes a `.vscode/settings.json` file with pre-configured settings for formatting, linting, and testing.

3. Install the pre-commit hooks as described in the "Pre-commit Hooks" section above.

With these settings and extensions, VSCode will

- Automatically format your code using Black and sort imports with isort on save
- Show Flake8 linting errors as you type
- Run pytest when you save Python files
- Provide YAML validation

The pre-commit hooks will ensure that all code passes these checks before being committed.
