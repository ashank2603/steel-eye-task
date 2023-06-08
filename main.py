from fastapi import FastAPI
from routes import trades

app = FastAPI(
    title = "SteelEye Task"
)

app.include_router(trades.router)