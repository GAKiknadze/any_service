from contextlib import asynccontextmanager

from dishka import make_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from .auth.infrastructure.provider import AuthProvider
from .auth.interfaces.api import exception_handlers as auth_exc_handlers
from .auth.interfaces.api import routers as auth_routers
from .common.infrastructure.providers import DatabaseProvider
from .common.interfaces.api import exception_handlers as common_exc_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = make_container(
        DatabaseProvider("sqlite+aiosqlite3://db.sqlite3"),
        AuthProvider("very_very_secret_key"),
        FastapiProvider(),
    )
    setup_dishka(container=container, app=app)

    yield

    app.state.dishka_container.close()


app = FastAPI(lifespan=lifespan)

# Common
app.add_exception_handler(Exception, common_exc_handlers.any_exc_handler)

# Auth
app.add_exception_handler(
    auth_exc_handlers.ContactAlreadyExistsExc,
    auth_exc_handlers.contact_already_exists_exc_handler,
)
app.add_exception_handler(
    auth_exc_handlers.InvalidCredentialsExc,
    auth_exc_handlers.invalid_credentials_exc_handler,
)
app.add_exception_handler(
    auth_exc_handlers.UserNotFoundExc, auth_exc_handlers.user_not_found_exc_handler
)
app.include_router(auth_routers.auth_router, prefix="/auth", tags=["auth"])
app.include_router(auth_routers.session_router, prefix="/session", tags=["auth"])
