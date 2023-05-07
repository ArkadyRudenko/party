from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return 'Hello!'


@app.get("/users/{user_id}")
def get_user(user_id):
    return user_id
