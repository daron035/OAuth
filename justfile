package_dir := "src"

# Show help message
help:
  just -l

# Install package with dependencies
install:
  uv sync --all-extras --all-groups

# Run pre-commit
lint:
	just _py pre-commit run --all-files

# Run tests
test *args:
  just _py pytest {{args}}

# Run app
run:
  python -Om {{package_dir}}

# Use uvicorn
uvicorn:
  just _py uvicorn src.presentation.api.main:init_api --factory --reload

# Build docker image
build:
	docker compose build

# Run app in docker container
up:
	docker compose --profile api up --build -d

# Stop docker containers
down:
	docker compose --profile api down

# Use Compose Watch
watch mode="build":
    #!/usr/bin/env bash
    set -euo pipefail

    case "{{mode}}" in
        "build")
            docker compose --profile watch build
            docker compose --profile watch up --watch
            docker image prune -f
            ;;
        "up")
            docker compose --profile watch up --watch
            ;;
        *)
            echo "Error: Unknown mode '{{mode}}'. Available: build, up"
            exit 1
            ;;
    esac

_py *args:
  uv run {{args}}
