from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Manufacturer(BaseModel):
    name: str
    country: str

class Laptop(BaseModel):
    id: int
    model: str
    ram: int  # в гигабайтах
    storage: int  # в гигабайтах
    category: str 
    rating: Optional[float] = None  # рейтинг ноутбука от 1 до 5
    manufacturer: Manufacturer

laptops: List[Laptop] = [
    Laptop(id=1, model="Dell XPS 13", ram=16, storage=512, category="Ультрабук", manufacturer=Manufacturer(name="Dell", country="USA")),
    Laptop(id=2, model="Apple MacBook Air", ram=8, storage=256, category="Ультрабук", manufacturer=Manufacturer(name="Apple", country="USA")),
    Laptop(id=3, model="HP Spectre x360", ram=16, storage=1024, category="Ультрабук", manufacturer=Manufacturer(name="HP", country="USA")),
    Laptop(id=4, model="Lenovo Legion 5", ram=16, storage=1024, category="Игровой", manufacturer=Manufacturer(name="Lenovo", country="China")),
]

@app.get("/laptops/", response_model=List[Laptop])
def read_laptops(ram: Optional[int] = Query(None, gt=0), storage: Optional[int] = Query(None, gt=0)):
    filtered_laptops = laptops
    if ram is not None:
        filtered_laptops = [l for l in filtered_laptops if l.ram >= ram]
    if storage is not None:
        filtered_laptops = [l for l in filtered_laptops if l.storage >= storage]
    return filtered_laptops

@app.get("/laptops/{laptop_id}", response_model=Laptop)
def read_laptop(laptop_id: int):
    laptop = next((l for l in laptops if l.id == laptop_id), None)
    if laptop is None:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return laptop

@app.post("/laptops/", response_model=Laptop)
def create_laptop(laptop: Laptop):
    if any(l.id == laptop.id for l in laptops):
        raise HTTPException(status_code=400, detail="Laptop ID already exists")
    laptops.append(laptop)
    return laptop

@app.put("/laptops/{laptop_id}", response_model=Laptop)
def update_laptop(laptop_id: int, laptop: Laptop):
    index = next((i for i, l in enumerate(laptops) if l.id == laptop_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Laptop not found")
    laptops[index] = laptop
    return laptop

@app.delete("/laptops/{laptop_id}", status_code=204)
def delete_laptop(laptop_id: int):
    index = next((i for i, l in enumerate(laptops) if l.id == laptop_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Laptop not found")
    laptops.pop(index)
    return None

@app.post("/laptops/{laptop_id}/rate/", response_model=Laptop)
def rate_laptop(laptop_id: int, rating: float):
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    laptop = next((l for l in laptops if l.id == laptop_id), None)
    if laptop is None:
        raise HTTPException(status_code=404, detail="Laptop not found")
    laptop.rating = rating
    return laptop
