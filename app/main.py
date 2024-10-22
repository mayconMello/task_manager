import traceback

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.configs import settings
from app.domain.errors import (
    ResourceNotFoundError,
    UserAlreadyExists,
    MaxFileSizeError,
    InvalidCredentialsError,
    OperationNotAllowedError,
)
from app.http.api import routers as api_routers

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.environment == "prd":
    app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(api_routers.router)

app.mount(
    f"/{settings.storage_url}/",
    StaticFiles(directory=settings.storage_path),
    name=settings.storage_url,
)


@app.middleware("http")
async def process_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except (ResourceNotFoundError, UserAlreadyExists, MaxFileSizeError) as error:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": error.message},
        )
    except (InvalidCredentialsError, OperationNotAllowedError) as error:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": error.message},
        )

    except Exception as error:
        print(error)
        print(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
