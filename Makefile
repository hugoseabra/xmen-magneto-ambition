DJANGO_SETTINGS_MODULE=project.settings
DOCKERFILE=conf/env/docker/Dockerfile
PROJECT_NAME=xmen-magneto-ambition
ENV_FILE=.env

.PHONY: help # Generate list of targets with descriptions
help:
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/ - \1 - \2/'

#--------------------------------------- DB -----------------------------------
.PHONY: db_delete # Deletes Sqlite3 database
db_delete:
	@rm -f db.sqlite3


.PHONY: db_update # Sets database to a predictable state
db_update:
	@python manage.py makemigrations
	python manage.py migrate

	# Custom report migrations
	@python manage.py loaddata 000_admin

#----------------------------------- DOCKER -----------------------------------
.PHONY: docker_build # Builds docker image
docker_build:
	@docker build -t $(PROJECT_NAME) -f $(DOCKERFILE) .

.PHONY: docker_run # Runs docker container
docker_run:
	# The container will be destroyed as soon as it stops due to '--rm'
	@docker run --rm --name $(PROJECT_NAME) -ti --env-file=$(ENV_FILE) -v $(pwd)/db.sqlite3:/app/db.sqlite3 -p 8000:8000 $(PROJECT_NAME)
