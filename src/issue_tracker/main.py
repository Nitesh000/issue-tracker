from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from issue_tracker.middleware.timer import timing_middleware
from issue_tracker.routes.issues import router as issue_router

app = FastAPI()


items = [
    {"id": 1, "name": "Item one"},
    {
        "id": 2,
        "name": "Item two",
    },
    {"id": 3, "name": "Item three"},
]

app.middleware("http")(timing_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "Ok"}


@app.get("/items")
def get_items(count: int = 100):
    return items[:count]


@app.get("/items/{item_id}")
def get_item_by_id(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}


@app.post("/items")
def add_item(item: dict):
    items.append(item)
    return items


app.include_router(issue_router)
