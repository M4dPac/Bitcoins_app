from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    id: int
    tg_id: int
    nick: str | None = None
    create_date: datetime
    wallet: Wallet
    sent_transaction: list[Transaction] = Field(default_factory=list)
    received_transaction: list[Transaction] = Field(default_factory=list)


class UserToUpdate(BaseModel):
    id: int
    # wallet: Wallet = None
    tg_id: int | None = None
    nick: str | None = None
    create_date: datetime | None = None


class UserToCreate(BaseModel):
    tg_id: int | None = None
    nick: str | None = None


class Wallet(BaseModel):
    id: int
    user: User | None = None
    balance: float = 0.0
    private_key: str
    address: str
    sent_transactions: list[Transaction] = Field(default_factory=list)
    received_transaction: list[Transaction] = Field(default_factory=list)


class Transaction(BaseModel):
    id: int
    sender: User | None = None
    receiver: User | None = None
    sender_wallet: Wallet | None = None
    receiver_wallet: Wallet | None = None
    sender_address: str | None = None
    receiver_address: str | None = None
    amount_btc_with_fee: float
    amount_btc_without_fee: float
    fee: float
    date_of_transaction: datetime
    tx_hash: str
