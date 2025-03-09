from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI()

class Mouse(BaseModel):
    id: int
    model: str
    dpi: int 
    wireless: bool  # беспроводная или проводная мышка
    manufacturer_name: str  
    manufacturer_country: str 

mice: List[Mouse] = [
    Mouse(id=1, model="Logitech MX Master 3", dpi=4000, wireless=True, manufacturer_name="Logitech", manufacturer_country="Switzerland"),
    Mouse(id=2, model="Razer DeathAdder V2", dpi=20000, wireless=False, manufacturer_name="Razer", manufacturer_country="USA"),
    Mouse(id=3, model="SteelSeries Rival 600", dpi=12000, wireless=False, manufacturer_name="SteelSeries", manufacturer_country="Denmark"),
    Mouse(id=4, model="Corsair Dark Core RGB", dpi=16000, wireless=True, manufacturer_name="Corsair", manufacturer_country="USA"),
]

@app.get("/mice/", response_model=List[Mouse])
def read_mice(dpi: Optional[int] = Query(None, gt=0), manufacturer: Optional[str] = None, country: Optional[str] = None):
    filtered_mice = mice
    if dpi is not None:
        filtered_mice = [m for m in filtered_mice if m.dpi >= dpi]
    if manufacturer is not None:
        filtered_mice = [m for m in filtered_mice if m.manufacturer_name.lower() == manufacturer.lower()]
    if country is not None:
        filtered_mice = [m for m in filtered_mice if m.manufacturer_country.lower() == country.lower()]
    return filtered_mice

@app.get("/mice/{mouse_id}", response_model=Mouse)
def read_mouse(mouse_id: int):
    mouse = next((m for m in mice if m.id == mouse_id), None)
    if mouse is None:
        raise HTTPException(status_code=404, detail="Mouse not found")
    return mouse

@app.post("/mice/", response_model=Mouse)
def create_mouse(mouse: Mouse):
    if any(m.id == mouse.id for m in mice):
        raise HTTPException(status_code=400, detail="Mouse ID already exists")
    mice.append(mouse)
    return mouse

@app.put("/mice/{mouse_id}", response_model=Mouse)
def update_mouse(mouse_id: int, mouse: Mouse):
    index = next((i for i, m in enumerate(mice) if m.id == mouse_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Mouse not found")
    mice[index] = mouse
    return mouse

@app.delete("/mice/{mouse_id}", status_code=204)
def delete_mouse(mouse_id: int):
    index = next((i for i, m in enumerate(mice) if m.id == mouse_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Mouse not found")
    mice.pop(index)
    return None

@app.get("/mice/stats/", response_model=Dict[str, int])
def get_mouse_statistics():
    stats = {}
    for mouse in mice:
        manufacturer = mouse.manufacturer_name
        stats[manufacturer] = stats.get(manufacturer, 0) + 1
    return stats
