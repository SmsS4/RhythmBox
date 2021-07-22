# pylint: skip-file
import os
from typing import List, Tuple, Optional, Dict

from fastapi import FastAPI, Request, HTTPException, File
from fastapi import Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse

from sharif_music.models import Music, PlayList, WebResult, AccountType, Account
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
    os.chdir("../web_ui")
    api.mount("/static", StaticFiles(directory="static"), name="static")

    templates = Jinja2Templates(directory="templates")

    # @api.exception_handler(HTTPException)
    # def validation_exception_handler(request, exc):
    #     print(request)
    #     return templates.TemplateResponse("not_found.html", {"request": request})
    @api.get('/validate_token')
    def validate_token(token: str) -> bool:
        return Api.server.validate_token(token)

    @api.get('/profile/get_account')
    def get_account(token:str) -> Account:
        return Api.server.get_account_by_token(token)

    @api.get("/music/{music_id}", )
    def get_music(music_id: str):
        file_like = open("/home/smss/Downloads/Telegram Desktop/wires.mp3", mode="rb")
        return StreamingResponse(file_like, media_type="audio/mp3")

    @api.get("/platform", response_class=HTMLResponse)
    def platform(request: Request, string: Optional[str]):
        return templates.TemplateResponse("platform.html", {"request": request, "string": string})

    @api.get("/search")
    def search(token: str, string: str) -> Dict[str, List[WebResult]]:
        return Api.server.serach(token, string)

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
            email: str = Form(...),
            name: str = Form(...),
    ) -> Tuple[str, bool]:
        print(username, password, email, name)
        return Api.server.create_account(username, password, email, name)

    @api.post("/profile/change_photo")
    def change_photo(token: str, file: UploadFile = Form(...)) -> int:
        return Api.server.change_photo(token, file)

    @api.get("/file")
    def get_file(file_id: int):
        file = Api.server.get_file_path(file_id)
        return StreamingResponse(open(file.path, "rb"), media_type=file.mime)

    def gen_file_url(file_id: int) -> str:
        return f"/file?file_id={file_id}"

    @api.get("/profile/{username}", response_class=HTMLResponse)
    def profile(username: str, request: Request):
        account = Api.server.get_account_by_username(username)
        if account is None:
            return templates.TemplateResponse("not_found.html", {"request": request})
        return templates.TemplateResponse(
            "profile.html",
            {
                "request": request,
                "name": account.name,
                "username": account.username,
                "email": account.email,
                "premium": "Yes :)" if account.account_type == AccountType.PREMIUM else "No :(",
                "publisher": "Yes :)" if account.publisher else "No :(",
                "description": account.description,
                "profile_url": "https://img.icons8.com/bubbles/100/000000/user.png" if not account.photo else gen_file_url(
                    account.photo.id),
            },
        )

    def make_premium(token: str) -> bool:
        return Api.server.make_premium(token)
    @api.post("/profile/upload_music")
    def add_music(token: str, name:str, file: UploadFile = Form(...)) -> bool:
        return Api.server.add_music(token, name, file)

    def search_music(music_name: str, music_genera: str) -> List[Music]:
        return Api.server.search_music(music_name, music_genera)

    def get_music(uid: str):
        music_info = Api.server.get_music(uid)
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
