
install:
	pip3 install --no-binary :all -r orius/requirements/development.txt

run:
	python3 main.py

container:
	docker-compose build
	docker-compose up
