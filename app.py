import fastapi

import pydantic_models
from database import crud

api = fastapi.FastAPI()


@api.get('/users/')
def get_all_users(skip: int = 0, limit: int = 10):
    return crud.get_users()


@api.get("/user/{user_id}")
def get_user(user_id: int):
    return crud.get_user_by_id(user_id)


@api.get("/user_by_tg_id/{tg_id}")
def get_user_by_tg_id(tg_id: int):
    return crud.get_user_by_tg_id(tg_id)


@api.post('/user/create')
def create_user(user: pydantic_models.UserToCreate = fastapi.Body()):
    return crud.create_user(**user)


@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.UserToUpdate = fastapi.Body()):
    return crud.update_user(user)


@api.delete("/user/{user_id}")
def delete_user(user_id: int = fastapi.Path()):
    return crud.delete_user(user_id)


# @api.get('/get_info_by_user_id/{user_id:int}')
# def get_info_about_user(user_id):
#     return crud.get_user_by_id(id=user_id)


@api.get('/get_user_balance/{user_id}')
def get_user_balance(user_id: int = fastapi.Path()):
    return crud.get_user_balance_by_id(user_id)


@api.get('/get_total_balance')
def get_total_balance():
    return crud.get_total_balance()


@api.post('/create_transaction')
def create_transaction(transaction: pydantic_models.Create_Transaction = fastapi.Body()):
    user = crud.get_user_by_tg_id(tg_id=transaction.sender_tg_id)
    return crud.create_transaction(
        sender_id=user.id,
        receiver_address=transaction.receiver_address,
        amount_btc_without_fee=transaction.amount_btc_without_fee
    )
# @api.get('/test')
# def test(request: fastapi.Request):
#     return request.cookies
