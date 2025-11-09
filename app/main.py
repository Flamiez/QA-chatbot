from contextlib import asynccontextmanager
import rootutils
from fastapi import FastAPI

rootutils.setup_root(__file__, indicator=['.git', 'pyproject.toml'], pythonpath=True)

from app.router import routerQ, routerI

app = FastAPI(title="API")
app.include_router(routerQ)
app.include_router(routerI)

@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run("app.main:app", reload=True)
    except ImportError:
        raise SystemExit("uvicorn is required to run the dev server. Install it and try again.")
