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
	docker compose --profile all build

# Run app in docker container
up:
	docker compose --profile api up --build -d

# Stop docker containers
down:
	docker compose --profile api down

# Up monitoring stack
monitoring:
  docker compose --profile grafana --profile prometheus up --build -d

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

# MinIO Client
mc command bucket='test-bucket':
    #!/usr/bin/env bash
    set -euo pipefail

    case "{{command}}" in
      "alias")
        echo -e "\033[1mmc alias set local http://localhost:9000 minioadmin minioadmin\033[0m"
        echo "Add MinIO service under 'local' alias."
        mc alias set local http://localhost:9000 minioadmin minioadmin
        ;;
      "mb")
        echo -e "\033[1mmc mb local/{{bucket}}\033[0m"
        echo "Create a new bucket: {{bucket}}"
        mc mb local/{{bucket}}
        ;;
      "ls")
        echo -e "\033[1mmc ls local\033[0m"
        echo "List all buckets"
        mc ls local
        ;;
      "lsb")
        echo -e "\033[1mmc ls local/{{bucket}}\033[0m"
        echo "List all contents of {{bucket}}"
        mc ls local/{{bucket}}
        ;;
      "rm")
        echo -e "\033[1mmc rm --recursive --force local/{{bucket}}\033[0m"
        echo "Remove all objects from bucket: {{bucket}}"
        mc rm --recursive --force local/{{bucket}}
        ;;
      "rb")
        echo -e "\033[1mmc rb --force local/{{bucket}}\033[0m"
        echo "Remove bucket - {{bucket}} and all its contents"
        mc rb --force local/{{bucket}}
        ;;
      *)
        echo "Unknown command: {{command}}"
        ;;
    esac


_py *args:
  uv run {{args}}
