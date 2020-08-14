# serving_model

Simple Flask API to serve a Text and Image vectorizer. This module uses pre-trained BERT for text vectorisation and a custom trained resnet101 for generating vectors for images and vectors.

## Valid Requests

All the requests sent to this API should be in consensus with the following format:

```json
[
    {
        "text": "this is a sentence too",
        "image": "https://kinsta.com/wp-content/uploads/2019/08/jpg-vs-jpeg.jpg"
    },{
        "text": "this is a sentence",
        "image": "https://kinsta.com/wp-content/uploads/2019/08/jpg-vs-jpeg.jpg"
    }
]
```

where, `text` represents a sentence that needes to be vectorised and `image` represents a valid Image URL. This should return a respone similar to the follwoing json:

```json
[
        {
            "image": "https://kinsta.com/wp-content/uploads/2019/08/jpg-vs-jpeg.jpg",
            "image_vector": [1,2,3,4],
            "text": "this is a sentence too",
            "text_vector": [1,2,3,4]
        },
        {
            "image": "https://kinsta.com/wp-content/uploads/2019/08/jpg-vs-jpeg.jpg",
            "image_vector": [1,2,3,4],
            "text": "this is a sentence",
            "text_vector": [1,2,3,4]
        }
    ]
```

If one doesn't want the image or text vector, it can simply be replaces with an empty string `""` and the response will not have the key for the relevant vector.

## Setup

To setup the required dependencies in an environment, simply run the command `make local-setup`.
To get the models from the connected google drive, simply run the command `make get-models`.

## Get Started

* Local Server
To start the server locally in an environment, simply run the command `make run-local-sever`. This command runs the setup commands first, followed by `unit-tests` and then starts a local sever in the terminal.

* Docker Server
To start the server through a docker image, simply run the command `make build-image`. Similar to the local server, this internally triggers the unit-tests before building the docker image.

Once the docker image is built, we can run the command `make run-container-server`. Pushing images to a cloud Registry has been left for future scope.

## Points of Improvement

* Slimmer Image can be used for docker
* Container takes some time to come live the first time, due to pre-trained BERT being loaded on the fly. This can be chnaged by having BERT locally as resnet101 is.
* When no text or image is specified in request, we are filtering out the vectors for empty string and a black image while formin g the response, this can be changed to not compute these vectors at all to improve the response time.
* CONTRIBUTING.txt is missing from the repo, it should be added.
* Commands for pushing to AWS ECR are available but are commented. This can be enabled in future to be able to push and pull from a remote registry.
