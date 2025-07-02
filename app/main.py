from fastapi import FastAPI, Security
from fastapi.openapi.utils import get_openapi
from app.auth.auth_router import router as auth_router
from app.db.database import init_db
from app.routes.inspection_router import router as inspection_router
from app.routes.report_router import router as report_router
from fastapi.security import HTTPBearer
from fastapi import Depends
from app.auth.dependencies import get_current_user
from app.db.models import User

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Quality Inspection System API is running."}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="AI Quality Inspection System API",
        version="1.0.0",
        description="API for AI-Enhanced Quality Inspection System",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Only add security globally if you want ALL endpoints protected
    # Otherwise, add security=[{"BearerAuth": []}] to each protected route
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

init_db()
app.include_router(auth_router, prefix="/auth")
app.include_router(inspection_router, prefix="/inspect")
app.include_router(report_router, prefix="/report")

@auth_router.get("/me", dependencies=[Security(HTTPBearer())])
def read_users_me(current_user: User = Depends(get_current_user)):
    ... 