import fastapi

import pydantic_models
from database import crud

api = fastapi.FastAPI()


@api.get('/users/')
def get_users(skip: int = 0, limit: int = 10):
    return crud.get_users()


# @api.post('/user/create')
# def create_user(user: pydantic_models.User = fastapi.Body()):
#     fake_database['users'].append(user)
#     return {'User Created!': user}


@api.get("/user/{user_id}")
def get_user(user_id: int):
    return crud.get_user_by_id(user_id)


@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.UserToUpdate = fastapi.Body()):
    return crud.update_user(user)


@api.delete("/user/{user_id}")
def delete_user(user_id: int = fastapi.Path()):
    return crud.delete_user(user_id)

# @api.get('/get_info_by_user_id/{id:int}')
# def get_info_about_user(id):
#     return crud.get_user_by_id(id=id)
#
#
# @api.get('/get_user_balance_by_id/{id:int}')
# def get_user_balance(id):
#     return fake_database['users'][id - 1]['balance']
#
#
# @api.get('/get_total_balance')
# def get_info_about_user():
#     total_balance: float = 0.0
#     for user in fake_database['users']:
#         total_balance += pydantic_models.User(**user).balance
#     return total_balance
#
#
# @api.get('/test')
# def test(request: fastapi.Request):
#     return request.cookies
