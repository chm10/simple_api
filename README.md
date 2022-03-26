# simple_api
Simple test api using Flask

# How to run
Download the repository.
```bash
git clone --depth 1 git@github.com:chm10/simple_api.git
```

Go to folder.
```bash
cd simple_api
```

Use `docker-compose`.

To run 
```bash
docker-compose up -d
```

Go to your favorite browser `localhost:5004`. Will be available an Swagger and documentation.

# To use ngrok
Download the program from website and run.

```bash
ngrok http http://localhost:5004
```

Copy the link and paste on https://ipkiss.pragmazero.com/.
Run the test. 

To down the container simple_api.
```bash
docker-compose down
```

To free space.
```bash
docker rmi simple_api_api
```