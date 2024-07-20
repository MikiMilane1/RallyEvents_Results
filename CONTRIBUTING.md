### How to run the Dockerfile locally
```
docker build -t <CONTAINER NAME> .
docker run -dp 5007:5000 -v ${PWD}:/app <CONTAINER NAME>
```

### How to deploy on Render
```
Add the SECRET_KEY variable from the .env file as an environment variable
```

