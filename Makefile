.PHONY: build run shell test help

IMAGE := modern-graphics
DOCKER_RUN := docker run --rm -it --ipc=host --init
OUTPUT_DIR := $(shell pwd)/output

help:
	@echo "Modern Graphics - Docker targets"
	@echo ""
	@echo "  make build     Build the Docker image"
	@echo "  make run      Run modern-graphics (use ARGS='create --layout hero ...')"
	@echo "  make shell    Interactive bash in container"
	@echo "  make test     Run smoke tests"
	@echo ""
	@echo "Example: make run ARGS='create --layout hero --headline \"Hello\" --png --output ./output/hero.png'"

build:
	docker build -t $(IMAGE) .

run:
	@mkdir -p $(OUTPUT_DIR)
	$(DOCKER_RUN) -v $(OUTPUT_DIR):/app/output -w /app $(IMAGE) $(ARGS)

shell:
	$(DOCKER_RUN) -v $(OUTPUT_DIR):/app/output -w /app --entrypoint /bin/bash $(IMAGE)

test:
	$(DOCKER_RUN) -v $(PWD):/app -w /app --entrypoint /bin/bash $(IMAGE) -c "pip install pytest -q && pytest -q tests/smoke/test_overhaul_phase1_smoke.py tests/smoke/test_layout_strategy_smoke.py tests/smoke/test_create_cli_phase3_smoke.py tests/smoke/test_create_story_regression_phase7_smoke.py tests/smoke/test_export_phase4_smoke.py tests/smoke/test_cli_migration_phase5_smoke.py tests/smoke/test_export_presets_phase6_smoke.py"
