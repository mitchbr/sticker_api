from fastapi import FastAPI
import uvicorn
import ssl

from src.routers.sticker import StickerRouter
from src.routers.stick import StickRouter
from src.routers.user import UserRouter


app = FastAPI()

stickers_router = StickerRouter()
app.include_router(stickers_router.router)

sticks_router = StickRouter()
app.include_router(sticks_router.router)

users_router = UserRouter()
app.include_router(users_router.router)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("/path/to/cert.pem", keyfile="/path/to/key.pem")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl=ssl_context)
