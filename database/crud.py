import bit

import pydantic_models
from database.db import *


def to_dict(x: db.Entity):
    return x.to_dict(with_collections=True)


@db_session
def create_wallet(user: User = None,
                  private_key: str = None,
                  testnet: bool = False
                  ):
    raw_wallet = bit.Key(private_key) if not testnet else bit.PrivateKeyTestnet(private_key)
    wallet = Wallet(user=user, private_key=raw_wallet.to_wif(), address=raw_wallet.address)
    return wallet


@db_session
def create_user(
        tg_id: int,
        nick: str = None,
        wallet: Wallet = None,
        testnet: bool = False
):
    wallet = wallet or create_wallet(testnet=testnet)
    data = {'tg_id': tg_id, 'wallet': wallet}
    if nick is not None:
        data['nick'] = nick
    user = User(**data)
    return to_dict(user)


@db_session
def create_transaction(
        sender_id: int,
        receiver_address: str,
        amount_btc_without_fee: float,
        fee: float | None = None,
):
    """
    :param sender_id: User.id
    :param amount_btc_without_fee:  количество биткоинов исключая комиссию, значение в сатоши
    :param receiver_address: адрес получателя, строка с адресом
    :param fee: абсолютная комиссия, исчисляем в сатоши - необязательно.
    :param testnet: в тестовой сети ли мы работаем
    :return: Transaction object
    """
    sender = User[sender_id]
    wallet_of_sender = bit.wif_to_key(sender.wallet.private_key)
    sender.wallet.balance = wallet_of_sender.get_balance()
    if not fee:
        fee = bit.network.fees.get_fee() * 1000

    amount_btc_with_fee = amount_btc_without_fee + fee
    if amount_btc_with_fee > sender.wallet.balance:
        return f'Too low balance: {sender.wallet.balance} need {amount_btc_with_fee}'

    output = [(receiver_address, amount_btc_without_fee, 'satoshi')]
    tx_hash = wallet_of_sender.send(output, fee, absolute_fee=True)
    transaction = Transaction(sender=sender,
                              sender_wallet=sender.wallet,
                              fee=fee,
                              sender_address=sender.wallet.address,
                              receiver_address=receiver_address,
                              amount_btc_with_fee=amount_btc_with_fee,
                              amount_btc_without_fee=amount_btc_without_fee,
                              tx_hash=tx_hash)
    return to_dict(transaction)


@db_session
def update_all_wallets():
    for wallet in Wallet.select():
        update_balance(wallet)
        print(wallet.address, wallet.balance)
    return True


@db_session
def update_balance(wallet: pydantic_models.Wallet):
    key = bit.wif_to_key(wallet.private_key)
    wallet.balance = key.get_balance()
    return wallet.balance


@db_session
def get_user_balance_by_id(user_id: int):
    wallet = User[user_id].wallet
    update_balance(wallet)
    return wallet.balance


@db_session
def get_total_balance() -> float:
    update_all_wallets()
    return sum(w.balance for w in Wallet.select())


@db_session
def get_users() -> list[pydantic_models.User]:
    return [get_user_info(user) for user in User.select()]


@db_session
def get_user_by_id(user_id: int):
    return get_user_info(User[user_id])


@db_session
def get_user_info(user: pydantic_models.User):
    data = to_dict(user)
    data['wallet'] = get_wallet_info(user.wallet)
    return data


@db_session
def get_user_by_tg_id(tg_id: int):
    return User.select(lambda u: u.tg_id == tg_id).first()


@db_session
def get_transaction_info(transaction: pydantic_models.Transaction):
    return transaction.to_dict(related_objects=True)


@db_session
def get_wallet_info(wallet: pydantic_models.Wallet):
    update_balance(wallet)
    return to_dict(wallet)


@db_session
def update_user(user: pydantic_models.UserToUpdate):
    db_user = User[user['id']]
    for k, v in user.items():
        setattr(db_user, k, v)
        return to_dict(db_user)


@db_session
def delete_user(user_id: int):
    User[user_id].delete()
    return True

# wallet = Key(config.PRIVATE_KEY)
