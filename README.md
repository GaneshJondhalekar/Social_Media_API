
# Social Networking Application API

This project is a social networking application API built using Django Rest Framework. It includes user authentication, search functionality, and friend request features.


## Features

- User Signup and Login(Using valid email)
- Search Users by Email and Name
- API to send/accept/reject friend request
- API to list friends(list of users who have accepted friend request)
- List pending friend requests(received friend request)


## Prerequisites
- Docker
- Docker Compose

## Installation

1. Clone the Repository

```bash
git clone https://github.com/GaneshJondhalekar/Social_Media_API.git

cd Social_Media_API
```
    
2. Build and Run the Docker Containers
```bash
docker-compose up --build
```
This will start the Django application on http://localhost:8000.


3. Project Migrations(If required)
```bash
docker-compose run web python manage.py makemigrations

docker-compose run web python manage.py migrate

```

## API Endpoints

- User Signup: `POST /accounts/register`
- User Login: `POST /accounts/login/`
- Search Users: `GET /accounts/search/?keyword=s`
- Send Friend Request: `POST /friend_request/send/`
- Accept/Reject Friend Request: `PATCH /friend_request/accept_reject/`
- List Friends: `GET /friend_request/list_friends/`
- List Pending Friend Requests: `GET /friend_request/pending/`

