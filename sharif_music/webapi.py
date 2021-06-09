# pylint: skip-file
import os
from typing import List, Tuple

from fastapi import FastAPI, Request
from fastapi import Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sharif_music.models import Music, Quality, PlayList
from sharif_music.server import Server


class Api:
    server: Server
    api: FastAPI


def init_api(server: Server) -> FastAPI:
    Api.server = server
    Api.api = FastAPI()

    api = Api.api

    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8000",
    ]

    api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    os.chdir("/web_ui")
    api.mount("/static", StaticFiles(directory="static"), name="static")

    templates = Jinja2Templates(directory="templates")

    @api.get("/", response_class=HTMLResponse)
    def home_page(request: Request):
        return templates.TemplateResponse("home.html", {"request": request})

    @api.post("/login")
    def login(username: str = Form(...), password: str = Form(...)) -> str:
        return Api.server.login(username, password)

    @api.post("/register")
    def register(
        username: str = Form(...),
        password: str = Form(...),
        phone: str = Form(...),
        name: str = Form(...),
    ) -> Tuple[str, bool]:
        return Api.server.create_account(username, password, phone, name)

    @api.get("/profile/{username}", response_class=HTMLResponse)
    def profile(username: str, request: Request):
        account = Api.server.get_account_by_username(username)
        if account is None:
            return templates.TemplateResponse("not_found.html", {"request": request})
        return templates.TemplateResponse(
            "profile.html",
            {"request": request, "name": account.name, "username": account.username},
        )

    def make_premium(token: str) -> bool:
        return Api.server.make_premium(token)

    def add_music(token: str) -> bool:
        raise NotImplementedError()
        return Api.server.add_music(token, None)

    def search_music(music_name: str, music_genera: str) -> List[Music]:
        return Api.server.search_music(music_name, music_genera)

    def get_music(uid: str, quality: Quality):
        music_info = Api.server.get_music(uid, quality)
        raise NotImplementedError()

    def add_playlist(token: str, name: str) -> bool:
        return Api.server.add_playlist(token, name)

    def get_playlist(uid: str) -> PlayList:
        return Api.server.get_playlist(uid)

    def add_owner_to_playlist(uid: str, username: str) -> bool:
        return Api.server.add_owner_to_playlist(uid, username)

    def add_music_to_playlist(token: str, playlist_uid: str, music_uid: str) -> bool:
        return Api.server.add_music_to_playlist(token, playlist_uid, music_uid)

    def remove_music_from_playlist(token: str, playlist_uid: str, music_uid) -> bool:
        return Api.server.remove_music_from_playlist(token, playlist_uid, music_uid)

    def get_default_playlist(token: str) -> PlayList:
        return Api.server.get_default_playlist(token)

    def follow_artis(token: str, artist: str) -> bool:
        return Api.server.follow_artis(token, artist)

    return api
