from fastapi import APIRouter, Depends

from pytonapi import AsyncTonapi

from config import API_KEY
from database import get_async_session

from models.transaction import Transaction
from models.user import User

from pydantic import Json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from datetime import datetime

import json


router = APIRouter(prefix='/txs_info', tags=['Работа с транзакциями'])

@router.get('/{account_id}', summary='На вход подается адрес кошелька на выход транзакции в формате JSON')
async def spawn_transactions(account_id: str,
                             session: AsyncSession = Depends(get_async_session)) -> Json:
    data = {} 
    tonapi = AsyncTonapi(api_key=API_KEY)
    account = await tonapi.accounts.get_events(account_id=account_id)
    try:
        new_user = User(
            wallet_address = account_id
        )
        session.add(new_user)
        await session.commit()
    except IntegrityError:
        print('LOL')
        await session.rollback()
    for event in account.events:
        preview = event.actions[0].simple_preview
        if preview.name.split(' ')[0] == 'Swap' and preview.accounts[0].name == 'STON.fi Dex':
            timestamp = datetime.fromtimestamp(event.timestamp)
            tx_hash = event.event_id
            currency_amount = event.actions[0].JettonSwap.amount_in
            ton_amount = event.actions[0].JettonSwap.ton_in
            amount = currency_amount if currency_amount else ton_amount
            tx_type = 'swap'
            status = event.actions[0].status
            user_id = await session.execute(select(User.id).where(User.wallet_address == account_id))
            user_id = user_id.scalar_one_or_none()
            try:
                new_transaction = Transaction(
                    user_id=user_id,
                    tx_hash=tx_hash,
                    amount=int(amount),
                    tx_type=tx_type,
                    tx_timestamp=timestamp,
                    status=status
                )
                session.add(new_transaction)
                await session.commit()
                data[tx_hash] = {
                    'user_id': user_id,
                    'amount': str(amount),
                    'tx_type': tx_type,
                    'tx_timestamp': timestamp,
                    'status': status
                    }
            except IntegrityError:
                data[tx_hash] = {
                    'user_id': user_id,
                    'amount': str(amount)   ,
                    'tx_type': tx_type,
                    'tx_timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    'status': status
                }
                await session.rollback()
    return json.dumps(data)