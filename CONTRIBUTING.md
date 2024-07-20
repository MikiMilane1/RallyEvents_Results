### How to run the Dockerfile locally
```
docker build -t <CONTAINER NAME> .
docker run -dp 5007:5000 -v ${PWD}:/app <CONTAINER NAME>