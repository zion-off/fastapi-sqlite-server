# Message Server

Simple messaging server built with FastAPI.

## Available endpoints

- POST /api/users: for user registration
- GET /api/users: for listing users
- POST /api/users/login: for user login
- POST /api/messages: for sending messages
- GET /api/messages: for listing incoming messages
- DELETE /api/messages/{message_id}: for deleting a message
- PATCH /api/messages/{message_id}: for updating a message

## Starting the server

```bash
source .venv/bin/activate
pip install requirements.txt
uvicorn main:app --reload
```

## Notes

The access token is stored in memory and is not refreshed. Once the client is logged in, they're in until the server restarts!