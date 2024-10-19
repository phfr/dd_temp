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

This project enforces standardized commit messages using Commitizen. While you can use the normal `git commit` command if you're familiar with the required format, we recommend using the interactive Commitizen command, especially if you're unsure about the formatting. Here's how to create a commit:

1. Stage your changes:
   ```
   git add .
   ```

2. To use the interactive Commitizen command (recommended for those unfamiliar with the format):
   ```
   cz commit
   ```

   Follow the prompts to create a standardized commit message. This will typically include:
   - Type of change (feat, fix, docs, style, refactor, test, chore)
   - Scope of the change (optional)
   - Short description
   - Longer description (optional)
   - Breaking changes (if any)
   - Issues closed (if any)

3. If you're familiar with the Commitizen format, you can use the standard git commit command:
   ```
   git commit -m "type(scope): short description"
   ```

   Make sure your commit message follows the Commitizen format to pass the pre-commit hooks.

Example of a commit message created with Commitizen:

```
feat(auth): add user authentication system

- Implement JWT token-based authentication
- Add login and logout endpoints
- Create user model and database migrations

BREAKING CHANGE: API now requires authentication for most endpoints
```

Using Commitizen ensures that all commit messages follow a consistent format, which helps with generating changelogs and understanding the project history. If you're ever unsure about the correct format, use the `cz commit` command for guidance.

## Questions?

If you have any questions or need further clarification, please open an issue or contact the maintainers.

## Code Style, Linting, and VSCode Setup

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

With these settings and extensions, VSCode will:
- Automatically format your code using Black and sort imports with isort on save
- Show Flake8 linting errors as you type
- Run pytest when you save Python files
- Provide YAML validation

The pre-commit hooks will ensure that all code passes these checks before being committed.
