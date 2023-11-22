#Beispiel: http://127.0.0.1:8000/search?gemaindename=Opfikon
import uvicorn
from fastapi import FastAPI

app = FastAPI()

d = {}
file = open("PLZO_CSV_LV95.csv", encoding="utf-8")
next(file)

for line in file:
    data = line.strip().split(";")
    ortschaft = data[0]
    plz = data[1]
    zusatzziffer = data[2]
    gemaindename = data[3]
    BFS = data[4]
    kanton = data[5]
    E = data[6]
    N = data[7]
    sprache = data[8]

    if gemaindename not in d:
        d[gemaindename] = []  # Создаем список для каждого уникального gemaindename

    d[gemaindename].append({  # Добавляем данные в список для данного gemaindename
        "ortschaft": ortschaft,
        "plz": plz,
        "zusatzziffer": zusatzziffer,
        "kanton": kanton,
        "gemaindename": gemaindename,
        "BFS-Nr": BFS,
        "E": E,
        "N": N,
        "sprache": sprache
    })

file.close()

@app.get("/search")
async def search(gemaindename: str):
    if gemaindename in d:
        return d[gemaindename]
    else:
        return {"error": "not found"}

uvicorn.run(app, host="127.0.0.1", port=8000)
