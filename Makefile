default: help

.PHONY: help
help: ## display this help message
	@echo "Please use \`make <target>\` where <target> is one of:"
	@grep -h '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m%-15s\033[0m%s\n", $$1, $$2}'

.PHONY: clean
clean: ## clean up temp & local build files (FRONTEND make clean + BACKEND make clean)
	make -C frontend clean
	make -C backend clean

.PHONY: dist
dist: ## build a docker image, push to Heroku Container Registry and release to the site
	heroku login
	heroku container:login
	heroku container:push -a foodbank-southlondon web
	heroku container:release -a foodbank-southlondon web

.PHONY: docker
docker: ## run the application locally with production settings using gunicorn inside docker (docker build & docker run)
	docker build -t foodbank-southlondon:latest .
	docker run -p 80:8080 -e FLASK_ENV=production -e PORT=8080 --env-file backend/production.env foodbank-southlondon:latest

.PHONY: install
install:  ## install the frontend and backend applications' dependencies locally (FRONTEND make install & BACKEND make install)
	make -C frontend install
	make -C backend install

.PHONY: run
run: ## run the application in development mode locally using the builtin Flask webserver (FRONTEND make build + BACKEND make run)
	make -C frontend build
	make -C backend run
