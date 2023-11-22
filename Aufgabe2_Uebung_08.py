#Пример: http://localhost:8000/wgs84lv95?lng=600000&lat=200000
import uvicorn
from fastapi import FastAPI, Query
from pyproj import Transformer

app = FastAPI()

# Создаем функцию для преобразования координат из LV95 в WGS84
def lv95_to_wgs84(lng: float, lat: float):
    transformer = Transformer.from_crs("EPSG:2056", "EPSG:4326", always_xy=True)
    wgs84_lng, wgs84_lat = transformer.transform(lng, lat)
    return {"wgs84_lng": wgs84_lng, "wgs84_lat": wgs84_lat}

# Создаем функцию для преобразования координат из WGS84 в LV95
def wgs84_to_lv95(lng: float, lat: float):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2056", always_xy=True)
    lv95_lng, lv95_lat = transformer.transform(lng, lat)
    return {"lv95_lng": lv95_lng, "lv95_lat": lv95_lat}

# Определяем эндпоинты для обоих преобразований
@app.get("/wgs84lv95")
async def wgs84_lv95(lng: float = Query(..., description="Долгота в формате LV95"), lat: float = Query(..., description="Широта в формате LV95")):
    return lv95_to_wgs84(lng, lat)

@app.get("/lv95wgs84")
async def lv95_wgs84(lng: float = Query(..., description="Долгота в формате WGS84"), lat: float = Query(..., description="Широта в формате WGS84")):
    return wgs84_to_lv95(lng, lat)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)