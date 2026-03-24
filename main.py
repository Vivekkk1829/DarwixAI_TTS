from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from core import process_text  
app = FastAPI()
templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
    request,
    "index.html",
    {"request": request}
)


@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, text: str = Form(...)):
    result = process_text(text)
    print(result)

    return templates.TemplateResponse(request,"index.html", {
        "request": request,
        "emotion": result["emotion"],
        "intensity": result["intensity"],
        "params": result["voice_params"],
        "text": text
    })
    


@app.get("/audio")
def get_audio():
    return FileResponse("output.mp3", media_type="audio/mpeg")