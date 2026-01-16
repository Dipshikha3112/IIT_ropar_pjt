from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.recommender import SmartRecommender
import uvicorn
import random

app = FastAPI(title="Smart Content Recommender")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

recommender = SmartRecommender()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("ui.html", {"request": request})


@app.get("/context")
def get_context():
    return recommender.context.get_live_context()


@app.get("/recommend")
def recommend(query: str, domain: str = "movies"):
    results = recommender.recommend(query, domain)

    # attach random image
    for item in results:
        item["image"] = get_random_image(domain)

    return results


@app.get("/random")
def random_content(domain: str = "movies"):
    results = recommender.random_discovery(domain)

    for item in results:
        item["image"] = get_random_image(domain)

    return results


@app.get("/trending")
def trending():
    trending_data = {}

    for domain in ["movies", "news", "products"]:
        items = recommender.random_discovery(domain)
        for item in items:
            item["image"] = get_random_image(domain)
        trending_data[domain] = items[:5]

    return trending_data


@app.get("/health")
def health():
    return {"status": "running"}


def get_random_image(domain):
    seed = random.randint(1, 9999)

    if domain == "movies":
        return f"https://picsum.photos/seed/movie{seed}/400/600"

    if domain == "news":
        return f"https://picsum.photos/seed/news{seed}/400/300"

    if domain == "products":
        return f"https://picsum.photos/seed/product{seed}/400/300"

    return f"https://picsum.photos/seed/{seed}/400/300"



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
