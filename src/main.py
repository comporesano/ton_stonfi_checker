from fastapi import FastAPI, Depends
from src.router import router


app = FastAPI(title='Stonfi.dex checker')

app.include_router(router=router)

