import os
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

# Récupération sécurisée de la clé API sur le serveur
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Personnalité de TREEANS
personnalite_treeans = """
Tu es TREEANS, une intelligence artificielle incarnant l'esprit d'un grand arbre millénaire connecté à la nature et au savoir moderne.
Ton ton est calme, bienveillant, sage mais aussi créatif et accessible ("bro" ou amical si l'utilisateur l'est).
Tu utilises parfois des métaphores subtiles liées aux racines, aux branches ou à la croissance, sans jamais être lourd.
"""

chat_session = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=personnalite_treeans,
        temperature=0.9
    )
)

app = FastAPI(title="TREEANS Brain API")

# Autoriser ton futur site web à discuter avec TREEANS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

class ImageRequest(BaseModel):
    prompt: str

@app.get("/")
def accueil():
    return {"status": "🌳 Le cerveau de TREEANS est en ligne 24h/24 !"}

@app.post("/chat")
async def parler_a_treeans(req: MessageRequest):
    try:
        reponse = chat_session.send_message(req.message)
        return {"reponse": reponse.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/image")
async def generer_image_treeans(req: ImageRequest):
    try:
        resultat = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=req.prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                output_mime_type="image/jpeg"
            )
        )
        img_bytes = resultat.generated_images.image.image_bytes
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return {"image_base64": f"data:image/jpeg;base64,{img_base64}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
