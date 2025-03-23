import os
from fastapi import FastAPI, status, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from model import Aranhaverso
from typing import Optional, Any

app = FastAPI(title="API do Aranhaverso", version="0.0.1", description="Mostra os homens-aranhas do aranhaverso")

app.mount("/static", StaticFiles(directory="static"), name="static")

homens_aranhas = {
    1: {
        "nome": "Miles Morales",
        "idade": 17,
        "cores_uniforme": "Preto com detalhes em vemelho",
        "poderes": "Choques elétricos, camuflagem, sentido aranha, agilidade e superforça",
        "personalidade": "Determinado, humilde, inseguro e empatico",
        "universo": "Terra-1610 (Ultimante Marvel Universe)",
        "foto": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/5b8d2b12-21e8-4931-8a6d-fb9ecdd60383/de8mwh8-76a795a2-e86d-4116-988f-cc0c87e2957f.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzViOGQyYjEyLTIxZTgtNDkzMS04YTZkLWZiOWVjZGQ2MDM4M1wvZGU4bXdoOC03NmE3OTVhMi1lODZkLTQxMTYtOTg4Zi1jYzBjODdlMjk1N2YucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.dmLtNLaJ9izmj0o_G5VHdb15B4IsgAtplw-8MsDvTz0"
    },

    2: {
        "nome": "Peter Benjamin Parker",
        "idade": 25,
        "cores_uniforme": "Vermelho com detalhes em azul",
        "poderes": "Força sobre-humana, sentido aranhha, lançamento de teias e agilidade",
        "personalidade": "Responsável, humos sarcático e confiante",
        "universo": "Terra-616 (Marvel principal)",
        "foto": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/bb677f07-6aa4-47b7-b56d-42896aaf50d9/dfkico5-44b156e3-cde3-4bf0-8031-39b16eeebe47.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2JiNjc3ZjA3LTZhYTQtNDdiNy1iNTZkLTQyODk2YWFmNTBkOVwvZGZraWNvNS00NGIxNTZlMy1jZGUzLTRiZjAtODAzMS0zOWIxNmVlZWJlNDcucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.NhGenXFaPGP89Ra1va3bDcRsOoh1y9mtJwyMm0oZ2Xw"
    },

    3: {
        "nome": "Miguel O'Hara (Spider-Man 2099)",
        "idade": 30,
        "cores_uniforme": "Azul escuro com detalhes em vermelho brilhante",
        "poderes": "Força sobre-humana, garras, visão de águia, agilidade aprimorada e manipulação do DNA",
        "personalidade": "Determinado e resiliente, cínico, anti-herói",
        "universo": "Terra-928 (Marvel 2099)",
        "foto": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/5b8d2b12-21e8-4931-8a6d-fb9ecdd60383/dfzaixl-fd91f627-69b1-4abf-97a6-fea48795635d.png/v1/fill/w_1280,h_1540/across_the_spider_verse_miguel_o_hara_png_by_metropolis_hero1125_dfzaixl-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTU0MCIsInBhdGgiOiJcL2ZcLzViOGQyYjEyLTIxZTgtNDkzMS04YTZkLWZiOWVjZGQ2MDM4M1wvZGZ6YWl4bC1mZDkxZjYyNy02OWIxLTRhYmYtOTdhNi1mZWE0ODc5NTYzNWQucG5nIiwid2lkdGgiOiI8PTEyODAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.6x77Q2FOH5XGyJ-ZJImN-7l-vTNOQbSDJ03uS5WqHSk",
    },

    4: {
        "nome": "Peter Parker (The Amazing Spider-Man)",
        "idade": 19,
        "cores_uniforme": "Vermelho e azul, com textura detalhada e olhos brancos",
        "poderes": "Força sobre-humana, agilidade aprimorada, fator de cura, habilidade de escalar paredes e lançadores de teia artificiais",
        "personalidade": "Inteligente, sarcástico, emocionalmente intenso e determinado",
        "universo": "Terra-120703",
        "foto": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/ecc902ea-1ffc-4fa2-9a5b-bb62cc09a029/dg6unf0-06586030-a27d-40e5-bc86-b6d064ca3f11.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2VjYzkwMmVhLTFmZmMtNGZhMi05YTViLWJiNjJjYzA5YTAyOVwvZGc2dW5mMC0wNjU4NjAzMC1hMjdkLTQwZTUtYmM4Ni1iNmQwNjRjYTNmMTEucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.Fexo2PnvHRdSWCFJXAFWCBR3SWKpK50kFJPgt_vjc3E"
    },

    5: {
        "nome": "Gwen Stacy (Spider-Woman)",
        "idade": 17,
        "cores_uniforme": "Branco, preto e detalhes em rosa e azul",
        "poderes": "Força sobre-humana, agilidade aprimorada, sentido aranha, habilidade de escalar paredes e reflexos aguçados",
        "personalidade": "Independente, corajosa, leal e espirituosa",
        "universo": "Terra-65",
        "foto": "https://images.twinkl.co.uk/tw1n/image/private/t_630/u/ux/gwen-pose-3_ver_1.png"
    }

}

templates = Jinja2Templates(directory='templates')

def fake_db():
    try:
        print("Conectando com o banco de dados.")
    finally:
        print("Fechando a conexão com o banco de dados.")

@app.get("/aranhas")
async def get_homens_aranhas(db: Any = Depends(fake_db)):
    return homens_aranhas

@app.get("/aranhas/{homens_aranhas_id}", description="Torna um homem-aranha individual", summary="Retorna um homem-aranha")
async def get_homens_aranhas(homens_aranhas_id: int):
    if homens_aranhas_id in homens_aranhas:
        homem_aranha = homens_aranhas[homens_aranhas_id]
        return homem_aranha
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe um homem-aranha com o id {homens_aranhas_id}")

@app.get("/", response_class=HTMLResponse)
async def aranhaverso_page(request: Request, id: Optional[int] = None):
    homem_aranha = None
    erro = None
    
    if id:
        if id in homens_aranhas:
            homem_aranha = homens_aranhas[id]
        else:
            erro = f"Não existe um Homem-Aranha com o ID {id}."

    return templates.TemplateResponse("aranhaverso.html", {"request": request, "titulo": "Aranhaverso", "homem_aranha": homem_aranha, "erro": erro})

@app.post("/aranhas", status_code=status.HTTP_201_CREATED)
async def post_homens_aranhas(homem_aranha: Optional[Aranhaverso] = None):
    next_id = len(homens_aranhas) + 1
    homens_aranhas[next_id] = homem_aranha
    del homem_aranha.id
    return homem_aranha

@app.put("/aranhas/{homens_aranhas_id}", status_code=status.HTTP_202_ACCEPTED)
async def put_homens_aranhas(homens_aranhas_id: int, homem_aranha: Aranhaverso):
    if homens_aranhas_id in homens_aranhas:
        homens_aranhas[homens_aranhas_id] = homem_aranha
        homem_aranha.id = homens_aranhas_id
        del homem_aranha.id
        return homem_aranha
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe um homem-aranha com o id {homens_aranhas_id}")
    
@app.delete("/aranhas/{homens_aranhas_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_homens_aranhas(homens_aranhas_id: int):
    if homens_aranhas_id in homens_aranhas:
        del homens_aranhas[homens_aranhas_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
@app.patch("/aranhas/{homens_aranhas_id}", status_code=status.HTTP_202_ACCEPTED)
async def patch_homens_aranhas_id(homens_aranhas_id: int, homem_aranha: Aranhaverso):
    if homens_aranhas_id in homens_aranhas:
        existing_homem_aranha = homens_aranhas[homens_aranhas_id]

        update_data = homem_aranha.dict(exclude_unset=True)
        existing_homem_aranha.update(update_data)

        return existing_homem_aranha
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe um homem-aranha com o id {homens_aranhas_id}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)