from src.api.audio import audio_router
from src.api.quiz import quiz_router
from src.api.users import users_router


all_routers = [
    quiz_router,
    users_router,
    audio_router
]