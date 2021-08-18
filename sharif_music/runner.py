"""
This class runs server and api
"""
import uvicorn  # type: ignore

from sharif_music.db_wrapper import DB
from sharif_music.server import Server
from sharif_music.webapi import init_api

if __name__ == "__main__":
    server = Server(DB())
    app = init_api(server)
    uvicorn.run(app, host="localhost", port=7000)
