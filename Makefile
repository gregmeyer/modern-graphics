.PHONY: build run shell test mcp gallery site help

IMAGE := modern-graphics
DOCKER_RUN := docker run --rm --ipc=host --init
OUTPUT_DIR := $(shell pwd)/output

help:
	@echo "Modern Graphics - Docker targets"
	@echo ""
	@echo "  make build     Build the Docker image"
	@echo "  make run      Run modern-graphics (use ARGS='create --layout hero ...')"
	@echo "  make shell    Interactive bash in container"
	@echo "  make test     Run smoke tests"
	@echo "  make mcp      Run MCP server in Docker (for AI clients)"
	@echo "  make gallery  Generate static gallery site in site/"
	@echo "  make site     Serve interactive gallery on http://localhost:8080"
	@echo ""
	@echo "Shorthand:"
	@echo "  ./generate <layout> [flags]   Auto-builds, defaults to PNG, outputs to ./output/"
	@echo ""
	@echo "Examples:"
	@echo "  make run ARGS='create --layout hero --headline \"Hello\" --png --output ./output/hero.png'"
	@echo "  ./generate hero --headline \"Hello\""

build:
	docker build -t $(IMAGE) .

run:
	@mkdir -p $(OUTPUT_DIR)
	$(DOCKER_RUN) -v $(OUTPUT_DIR):/app/output -w /app $(IMAGE) $(ARGS)

shell:
	$(DOCKER_RUN) -it -v $(OUTPUT_DIR):/app/output -w /app --entrypoint /bin/bash $(IMAGE)

test:
	$(DOCKER_RUN) -v $(PWD):/app -w /app --entrypoint /bin/bash $(IMAGE) -c "pip install pytest -q && pytest -q tests/smoke/test_overhaul_phase1_smoke.py tests/smoke/test_layout_strategy_smoke.py tests/smoke/test_create_cli_phase3_smoke.py tests/smoke/test_create_story_regression_phase7_smoke.py tests/smoke/test_export_phase4_smoke.py tests/smoke/test_cli_migration_phase5_smoke.py tests/smoke/test_export_presets_phase6_smoke.py"

mcp:
	@mkdir -p $(OUTPUT_DIR)
	$(DOCKER_RUN) -i -v $(OUTPUT_DIR):/app/output -w /app --entrypoint python $(IMAGE) -m modern_graphics.mcp_server

gallery:
	@mkdir -p site
	$(DOCKER_RUN) -v $(PWD)/site:/app/site -v $(PWD)/examples:/app/examples -w /app --entrypoint python $(IMAGE) -m modern_graphics.web.gallery --output /app/site

site: gallery
	@echo "Gallery site at http://localhost:8080"
	@mkdir -p $(OUTPUT_DIR)
	$(DOCKER_RUN) -p 8080:8080 -v $(PWD)/site:/app/site -v $(OUTPUT_DIR):/app/output -w /app --entrypoint python $(IMAGE) -m modern_graphics.web.app --port 8080
