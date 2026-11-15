# Contributing to MLX Control Center

Thank you for your interest in contributing! This guide explains how to set up your development environment and submit changes.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/timkusenko/mlx-control-center
   cd mlx-control-center
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install development tools**:
   ```bash
   pip install pytest pytest-cov black isort mypy
   ```

## Code Style

- **Format code** with `black`:
  ```bash
  black mlx_control tests
  ```

- **Sort imports** with `isort`:
  ```bash
  isort mlx_control tests
  ```

- **Type check** with `mypy`:
  ```bash
  mypy mlx_control --ignore-missing-imports
  ```

## Running Tests

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ -v --cov=mlx_control --cov-report=html
```

## Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes** and add tests for new functionality

3. **Run tests and linting**:
   ```bash
   pytest tests/
   black mlx_control tests
   isort mlx_control tests
   ```

4. **Commit with clear message**:
   ```bash
   git commit -m "feat: add cool feature"
   ```

5. **Push and create a pull request**:
   ```bash
   git push origin feature/my-feature
   ```

## Commit Message Convention

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation only
- `refactor:` — Code cleanup (no behavior change)
- `test:` — Test additions/changes
- `chore:` — Build, dependencies, etc.

Example: `feat: add model download progress bar`

## Pull Requests

When submitting a PR:

- **Description** — What problem does this solve?
- **Type** — Bug fix, feature, refactor, etc.
- **Testing** — How should this be tested?
- **Checklist**:
  - [ ] Tests pass
  - [ ] Code is formatted (`black`, `isort`)
  - [ ] No type errors (`mypy`)
  - [ ] Documentation updated (if needed)

## Questions?

Open a GitHub issue with your question. Maintainers will respond.

Thanks for contributing! 🎉
