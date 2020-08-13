# REGISTRY=xxxxxxxxxxxx
# REGION=us-east-1

###############
# Local Setup #
###############

local-setup:
	cd app && python3 -m pip install --no-cache-dir -r requirements.txt

get-models:
	dvc pull

##############################
# Running the server locally #
##############################

run-local-server:
	make get-models
	make local-setup
	make unit-test
	cd app && python3 application.py

#########
# tests #
#########

unit-test:
	cd app && python -m unittest discover -v -s tests/ -p 'test_*.py'

#############################################
# Building and running Docker image locally #
#############################################

build-image:
	make get-models
	make local-setup
	make unit-test
	docker build -t model_server .

run-container-server:
	docker stop model_server || true && docker rm model_server || true
	docker run -d -p 5000:5000 --name=model_server  model_server


#################################################
# Pushing and pulling Docker image from AWS ECR #
#################################################
# push-image:
# 	$(aws ecr get-login --no-include-email --region ${REGION})
# 	docker tag model_server ${REGISTRY}.dkr.ecr.${REGION}.amazonaws.com/model_server 
# 	docker push ${REGISTRY}.dkr.ecr.${REGION}.amazonaws.com/model_server

# pull-image:
# 	$(aws ecr get-login --no-include-email --region ${REGION})
# 	docker pull ${REGISTRY}.dkr.ecr.${REGION}.amazonaws.com/model_server
# 	docker tag ${REGISTRY}.dkr.ecr.${REGION}.amazonaws.com/model_server model_server 
