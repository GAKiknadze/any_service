from contextlib import asynccontextmanager

from dishka import make_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from src.auth.infrastructure.provider import AuthProvider
from src.common.infrastructure.providers import DatabaseProvider
from src.common.interfaces.api import exception_handlers as common_exc_handlers
from src.interfaces.api import api_router, exception_handlers
from src.profile.infrastructure.provider import ProfileProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    app.state.dishka_container.close()


app = FastAPI(lifespan=lifespan)

container = make_container(
    DatabaseProvider("sqlite+aiosqlite:///temp.db"),
    AuthProvider("very_very_secret_key"),
    ProfileProvider(),
    FastapiProvider(),
)
setup_dishka(container=container, app=app)

# Common
app.add_exception_handler(Exception, common_exc_handlers.any_exc_handler)

# Auth
app.add_exception_handler(
    exception_handlers.ContactAlreadyExistsExc,
    exception_handlers.contact_already_exists_exc_handler,
)
app.add_exception_handler(
    exception_handlers.InvalidCredentialsExc,
    exception_handlers.invalid_credentials_exc_handler,
)
app.add_exception_handler(
    exception_handlers.UserNotFoundExc, exception_handlers.user_not_found_exc_handler
)

# Connecting API router
app.include_router(api_router, prefix="/api")
