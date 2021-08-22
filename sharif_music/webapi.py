# pylint: skip-file
import os
from typing import List, Tuple, Optional, Dict

from fastapi import FastAPI, Request
from fastapi import Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sharif_music.models import (
    PlayList,
    WebResult,
    AccountType,
    Account,
    PlaylistWeb,
)
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
    @api.get("/validate_token")
    def validate_token(token: str) -> bool:
        return Api.server.validate_token(token)

    @api.get("/profile/get_account")
    def get_account(token: str) -> Optional[Account]:
        return Api.server.get_account_by_token(token)
    @api.get("/listen")
    def listen(token:str, music_id:int):
        print(token, music_id)
        Api.server.listen(token, music_id)
    @api.get("/music/{music_id}")
    def get_music(music_id: int):
        music = Api.server.get_music(music_id)
        return StreamingResponse(open(music.file.path, "rb"), media_type="audio/mp3")

    @api.get("/platform", response_class=HTMLResponse)
    def platform(request: Request, string: Optional[str]):
        return templates.TemplateResponse(
            "platform.html", {"request": request, "string": string}
        )

    @api.get("/search")
    def search(token: str, string: str) -> Dict[str, List[WebResult]]:
        return Api.server.serach(token, string)

    @api.get("/", response_class=HTMLResponse)
    def home_page(request: Request):
        return templates.TemplateResponse("home.html", {"request": request})

    @api.post("/login")
    def login(
        username: str = Form(...), password: str = Form(...)
    ) -> Tuple[str, Optional[Account]]:
        return Api.server.login(username, password)

    @api.post("/edit")
    def edit_profile(
        token: str = Form(...),
        name: str = Form(...),
        description: str = Form(...),
        req_publisher: str = Form(...),
        req_premium: str = Form(...),
    ):
        Api.server.edit(token, name, description)
        if req_publisher == "true":
            Api.server.request_publisher(token)
        if req_premium == "true":
            Api.server.request_premium(token)

    @api.post("/register")
    def register(
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        name: str = Form(...),
    ) -> Tuple[str, bool]:
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
                "premium": "Yes :)"
                if account.account_type == AccountType.PREMIUM
                else "No :(",
                "publisher": "Yes :)" if account.publisher else "No :(",
                "description": account.description,
                "profile_url": "https://img.icons8.com/bubbles/100/000000/user.png"
                if not account.photo
                else gen_file_url(account.photo.id),
            },
        )

    @api.post("/profile/upload_music")
    def add_music(
        token: str, name: str, genera: str, file: UploadFile = Form(...)
    ) -> bool:
        return Api.server.add_music(token, name, file, genera)

    @api.post("/addpl")  # done
    def add_playlist(token: str = Form(...), name: str = Form(...)) -> None:
        Api.server.add_playlist(token, name)

    @api.post("/delpl")  # done
    def add_playlist(
        token: str = Form(...), playlist_id: int = Form(...)
    ) -> Optional[str]:
        return Api.server.remove_playlist(token, playlist_id)

    @api.get("/getpl")  # done
    def get_playlist(uid: int) -> PlayList:
        return Api.server.get_playlist(uid)

    @api.post("/add_owener_pl")  # done
    def add_owner_to_playlist(
        token: str = Form(...), uid: int = Form(...), username: str = Form(...)
    ) -> Optional[str]:
        return Api.server.add_owner_to_playlist(token, uid, username)

    @api.post("/add_music_pl")  # done
    def add_music_to_playlist(
        token: str = Form(...),
        playlist_uid: int = Form(...),
        music_uid: int = Form(...),
    ) -> Optional[str]:
        return Api.server.add_music_to_playlist(token, playlist_uid, music_uid)

    @api.post("/remove_music_pl")  # done
    def remove_music_from_playlist(
        token: str = Form(...),
        playlist_uid: int = Form(...),
        music_uid: int = Form(...),
    ) -> Optional[str]:
        return Api.server.remove_music_from_playlist(token, playlist_uid, music_uid)

    @api.get("/get_my_pl")  # done
    def get_my_playlists(username: str) -> List[PlaylistWeb]:
        return Api.server.get_my_playlists(username)

    @api.post("/follow")
    def follow(token: str = Form(...), username: str = Form(...)):
        return Api.server.follow(token, username)

    @api.post("/checkfollow")
    def follow(token: str = Form(...), username: str = Form(...)):
        return Api.server.checkfollow(token, username)

    @api.post("/share")
    def share(playlist_id: int = Form(...), username: str = Form(...)):
        Api.server.share(playlist_id, username)

    @api.get("/swm")
    def get_default_playlist(token: str) -> List[PlaylistWeb]:
        return Api.server.shared_with_me(token)

    return api
