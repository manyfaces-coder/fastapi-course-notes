from pydantic import BaseModel, Field, EmailStr, ConfigDict
from fastapi import FastAPI

app = FastAPI()

data = {
    "email": "aasd@mail.ru",
    "bio": None,
    "age": 12,
}

data_no_age = {
    "email": "aasd@mail.ru",
    "bio": None,
    "gender": "male",
    "birthday": "2000"
}


class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=10)

    model_config = ConfigDict(extra='forbid')


users = []


@app.post("/users")
def add_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "msg":"users added"}


@app.get("/users")
def get_user() -> list[UserSchema]:
    return users

class UserAgeSchema(UserSchema):
    age: int = Field(ge=0, le=130)


#
# def func(data_: dict):
#     data_["age"] += 1

#
# users = UserSchema(**data_no_age)
# print(repr(users))
