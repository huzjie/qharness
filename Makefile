.PHONY: install dev test lint doctor run serve docker

install:
	pip install -e .

dev:
	pip install -e ".[all]"

test:
	python -m unittest discover -s tests -v

lint:
	python -m py_compile qharness/*/*.py

doctor:
	qharness doctor

run:
	qharness run "创建一个 Flask TODO 应用，含增删改查接口" --provider mock

serve:
	qharness serve --port 8000

docker:
	docker build -t qharness:latest .
