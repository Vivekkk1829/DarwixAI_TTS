from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def home():
    return {"message":"Running Successfully"}

@app.post("/speak")
def speak(text :str):
    return {"Message":"Waiting to execute"}