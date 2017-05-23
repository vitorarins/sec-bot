version ?= latest
BOTNAME=edgar
IMAGE = sec-bot
RUN_PYTHON = docker run --rm --entrypoint python $(IMAGE)


guard-%:
	@ if [ "${${*}}" = "" ]; then \
                echo "Variable '$*' not set"; \
                exit 1; \
        fi

image:
	docker build -t $(IMAGE) .

run: image
	docker run --rm $(IMAGE)

test: image
	$(RUN_PYTHON) -m unittest sec_bot_test.py
