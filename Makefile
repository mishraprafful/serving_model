run-local-server:
	cd app && python3 application.py

local-setup:
	cd app && python3 -m pip install --no-cache-dir -r requirements.txt

get-models:
	dvc pull

build-image:
	docker build -t model_server .

run-container-server:
	docker stop model_server || true && docker rm model_server || true
	docker run -d -p 5000:5000 --name=model_server  model_server