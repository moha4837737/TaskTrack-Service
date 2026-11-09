IMAGE=tasktrack-api

build:
	docker build -t $(IMAGE) .

run:
	docker run -d --name $(IMAGE) -p 5000:5000 -v tasks-data:/data $(IMAGE)

stop:
	-docker stop $(IMAGE)
	-docker rm $(IMAGE)

test:
	pip install -r requirements.txt pytest && pytest -q

.PHONY: build run stop test
