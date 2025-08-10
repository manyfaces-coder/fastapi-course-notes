from fastapi import FastAPI

app = FastAPI()


@app.get("/", summary="Главная ручка", tags=["Основные ручки"])
def home():
    return "Hello World!!!"