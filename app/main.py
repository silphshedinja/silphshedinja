from typing import Optional
from fastapi import Depends, FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import urllib.request, json 

from database import SessionLocal, engine
import models

#Use Migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    num_pokemon = db.query(models.Pokemon).count()
    if num_pokemon == 0:
        with urllib.request.urlopen("https://raw.githubusercontent.com/pvpoke/pvpoke/b45275f9cd5e6dc00ef1678f274978326e4855f1/src/data/gamemaster/pokemon.json") as url:
            pokemons = json.load(url)
            for pokemon in pokemons:
                toadd = {
                    'dex': pokemon['dex'], 
                    'name': pokemon['speciesName'],
                    'types': str(pokemon['types']),
                    'released': pokemon['released'] 
                    }
                db.add(models.Pokemon(**toadd))
            db.commit()
            db.close()
    else:
        print("Pokemon already loaded")


templates = Jinja2Templates(directory="templates")


@app.get("/pokemon/", response_class=HTMLResponse)
async def movielist(
    request: Request, 
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db)
    ):
    pokemons = db.query(models.Pokemon).all()
    context = {"request": request, 'pokemons': pokemons}
    if hx_request:
        return templates.TemplateResponse("partials/table.html", context)
    return templates.TemplateResponse("index.html", context)