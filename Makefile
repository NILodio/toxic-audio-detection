# Makefile for running the Docker container

# Define variables
IMAGE_NAME = toxic-audio-detection/python_data_science
IMAGE_TAG = anaconda
CONTAINER_NAME = toxic-audio-detection-jupyter

# Define targets and their rules
.PHONY: run

run:
	docker run -d -p 8888:8888 -p 6006:6006 \
		-v $(shell pwd)/notebooks:/notebooks \
		-v $(shell pwd)/data:/data \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME):$(IMAGE_TAG)


.PHONY: format
format:
	python -m isort .
	python -m black .
	python -m ruff check . --fix

.PHONY: develop
develop: install
	python -m pre_commit install

.PHONY: build_notebook

build_notebook:
	@echo "Building development server..."
	@docker build -f Dockerfile.anaconda -t toxic-audio-detection/python_data_science:anaconda .
	@echo "Done!"

.PHONY: start_notebook

start_notebook:
	@echo "starting development server..."
	docker run -d -p 8888:8888 -p 6006:6006 \
		-v $(shell pwd)/notebooks:/notebooks \
		-v $(shell pwd)/data:/data \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "Done!"

.PHONY: stop_notebook
stop_notebook: clean_notebook
	@echo "stopping development server..."
	docker stop $(CONTAINER_NAME)
	@echo "Done!"


.PHONY: clean_notebook

clean: clean_notebook
	docker rm $(CONTAINER_NAME)


.PHONY: install
install:
	python -m pip install --upgrade pip
	python -m pip install --editable .
	python -m pip install -U -r requirements/requirements.dev.txt

.PHONY: develop
develop: install
	python -m pre_commit install

.PHONY: build_no_cache
build_no_cache:
	docker-compose build --no-cache

.PHONY: build
build:
	docker-compose --profile all build

.PHONY: up
up:
	docker-compose --profile all up --build -d

.PHONY: up-dev
up-dev:
	docker-compose --profile develop up --build -d

.PHONY: down
down:
	docker-compose --profile all down

.PHONY: clean
clean:
	docker-compose --profile all down
	docker-compose --profile all rm -f

.PHONY: delete
delete:
	docker rmi toxic-audio-detection/python_data_science:anaconda

.PHONY: cli
cli:
	docker compose run cli
