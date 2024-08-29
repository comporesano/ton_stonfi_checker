from fastapi import APIRouter, Depends

from pytonapi import AsyncTonapi

from src.config import API_KEY
from src.database import get_async_session

from src.models.transaction import Transaction
from src.models.user import User

from pydantic import Json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from datetime import datetime

import json


router = APIRouter(prefix='/txs_info', tags=['Работа с транзакциями'])
#example: time_from /UQCQ2ZY1vcjPRaaTnoGckmXEqTjoejtUtM8l9buDLjnGbU4X/?time_from=2024-08-28+09:16:19
@router.post('/{account_id}', summary='На вход подается адрес кошелька на выход транзакции в формате JSON')
async def spawn_transactions(account_id: str,
                             time_from: str = None,
                             time_to: str = None,
                             session: AsyncSession = Depends(get_async_session)) -> Json:
    data = {'data': {}} 
    tonapi = AsyncTonapi(api_key=API_KEY)
    account = await tonapi.accounts.get_events(account_id=account_id)
    try:
        new_user = User(
            wallet_address = account_id
        )
        session.add(new_user)
        await session.commit()
    except IntegrityError:
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
                data['data'][tx_hash] = {
                    'user_id': user_id,
                    'amount': str(amount),
                    'tx_type': tx_type,
                    'tx_timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    'status': status
                    }
            except IntegrityError:
                data['data'][tx_hash] = {
                    'user_id': user_id,
                    'amount': str(amount),
                    'tx_type': tx_type,
                    'tx_timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    'status': status
                }
                await session.rollback()

    aggregation_data = {'data': {}}
    
    if time_from:
        time_from = ' '.join(time_from.split('+'))
        timest_from = datetime.strptime(time_from, "%Y-%m-%d %H:%M:%S").timestamp()
    if time_to:
        time_to = ' '.join(time_to.split('+'))
        timest_to = datetime.strptime(time_to, "%Y-%m-%d %H:%M:%S").timestamp() 
    for tx_hash in data['data']:
        tx_data = data['data'][tx_hash]
        if time_from and not time_to:
            if timest_from <= datetime.strptime(tx_data['tx_timestamp'], "%Y-%m-%d %H:%M:%S").timestamp():
                aggregation_data['data'][tx_hash] = tx_data
        elif not time_from and time_to: 
            if datetime.strptime(tx_data['tx_timestamp'], "%Y-%m    -%d %H:%M:%S").timestamp() <= timest_to:
                aggregation_data['data'][tx_hash] = tx_data
        elif time_from and time_to:
            if timest_from > time_to:
                aggregation_data['data'] = {'INTERNAL SERVER ERROR: Upper limit less than down limit'}
            if timest_from <=   datetime.strptime(tx_data['tx_timestamp'], "%Y-%m-%d %H:%M:%S").timestamp() <= timest_to:
                aggregation_data['data'][tx_hash] = tx_data
        
    return json.dumps(data) if not time_from and not time_to else json.dumps(aggregation_data)