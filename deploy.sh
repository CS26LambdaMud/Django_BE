# build our heroku-ready local Docker image

sudo docker build -t adv_project -f Dockerfile .


# push your directory container for the web process to heroku
sudo heroku container:push web -a advtest


# promote the web process with your container 
sudo heroku container:release web -a advtest


# run migrations
sudo heroku run python3 manage.py migrate -a advtest