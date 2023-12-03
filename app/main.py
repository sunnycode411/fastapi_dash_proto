from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn

from dash_plots.test_graph import test_graph
from dash_plots.map_india import india_map_dash_app
from dash_plots.animated_india_map import animated_india_map_dash_app

app = FastAPI()

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Update with the URL of your Node.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


app.mount("/test_graph", WSGIMiddleware(test_graph().server))
app.mount("/india_map_graph", WSGIMiddleware(india_map_dash_app.server))
app.mount("/animated_india_map", WSGIMiddleware(animated_india_map_dash_app.server))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, timeout_keep_alive=300)