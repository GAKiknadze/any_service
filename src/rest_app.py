from contextlib import asynccontextmanager

from dishka import make_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from src.auth.infrastructure.provider import AuthProvider
from src.infrastructure.config import Settings
from src.infrastructure.providers import DatabaseProvider
from src.interfaces.api import api_router, exception_handlers
from src.profile.infrastructure.provider import ProfileProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    app.state.dishka_container.close()


app = FastAPI(lifespan=lifespan)

settings = Settings()  # type: ignore[call-arg]

container = make_container(
    DatabaseProvider(database_url=settings.db_uri),
    AuthProvider(secret_key=settings.secret_key),
    ProfileProvider(),
    FastapiProvider(),
)
setup_dishka(container=container, app=app)

# Common
app.add_exception_handler(Exception, exception_handlers.any_exc_handler)

# Auth
app.add_exception_handler(
    exception_handlers.ContactAlreadyExistsExc,
    exception_handlers.contact_already_exists_exc_handler,  # type: ignore[arg-type]
)
app.add_exception_handler(
    exception_handlers.InvalidCredentialsExc,
    exception_handlers.invalid_credentials_exc_handler,  # type: ignore[arg-type]
)
app.add_exception_handler(
    exception_handlers.UserNotFoundExc,
    exception_handlers.user_not_found_exc_handler,  # type: ignore[arg-type]
)

# Connecting API router
app.include_router(api_router, prefix="/api")
