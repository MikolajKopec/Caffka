
## Installation

Thanks to docker, you don't need much for run this project locally.

1. Install docker (Docker desktop for windows)
https://www.docker.com/products/docker-desktop/
2. Clone repository 
```
  git clone https://gitlab.com/mikolajkopec772/caffka.git
```
3. Set your own `.env` file in project folder. This is needed by docker to set up you database. 
Example:
```
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres_db
POSTGRES_PORT=5432
```
4. Run `docker-compose up -d --build`
5. Success! The app should be running on http://localhost:8000/
