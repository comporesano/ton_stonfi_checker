from pytonapi import AsyncTonapi

from config import API_KEY

import asyncio
import datetime


async def main() -> None:
    tonapi = AsyncTonapi(api_key=API_KEY, timeout=120)
    
    account_id = 'UQCQ2ZY1vcjPRaaTnoGckmXEqTjoejtUtM8l9buDLjnGbU4X'
    
    account = await tonapi.accounts.get_events(account_id=account_id)
    _ = [print(i, eve, eve.actions[0].simple_preview, eve.timestamp, eve.event_id, sep='\n') for i, eve in enumerate(account.events) if eve.actions[0].simple_preview.name.split(' ')[0] == 'Swap']

if __name__ == '__main__':
    asyncio.run(main())
    print(datetime.datetime.now().timestamp())
    print(datetime.datetime.now())