default:
    just --list;

setup:
    uv venv --clear

lint:
    uv pip install ruff
    uv run ruff format ./src && git add ./src && git commit -m "style: format source"
