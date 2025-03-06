from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Manufacturer(BaseModel):
    name: str
    country: str

class Refrigerator(BaseModel):
    id: int
    model: str
    capacity: float
    manufacturer: Manufacturer

refrigerators: List[Refrigerator] = [
    Refrigerator(id=1, model="LG InstaView", capacity=600.0, manufacturer=Manufacturer(name="LG Electronics", country="South Korea")),
    Refrigerator(id=2, model="Samsung Family Hub", capacity=700.0, manufacturer=Manufacturer(name="Samsung", country="South Korea")),
    Refrigerator(id=3, model="Whirlpool Side-by-Side", capacity=500.0, manufacturer=Manufacturer(name="Whirlpool", country="USA")),
    Refrigerator(id=4, model="Bosch Serie 4", capacity=400.0, manufacturer=Manufacturer(name="Bosch", country="Germany")),
]

@app.get("/refrigerators/", response_model=List[Refrigerator])
def read_refrigerators(
    model: Optional[str] = None,
    min_capacity: Optional[float] = Query(None, gt=0),
    max_capacity: Optional[float] = Query(None, gt=0),
    sort_by_capacity: Optional[bool] = False
):
    filtered_refrigerators = refrigerators

    if model:
        filtered_refrigerators = [fridge for fridge in filtered_refrigerators if model.lower() in fridge.model.lower()]
    
    if min_capacity is not None:
        filtered_refrigerators = [fridge for fridge in filtered_refrigerators if fridge.capacity >= min_capacity]

    if max_capacity is not None:
        filtered_refrigerators = [fridge for fridge in filtered_refrigerators if fridge.capacity <= max_capacity]

    if sort_by_capacity:
        filtered_refrigerators.sort(key=lambda x: x.capacity)

    return filtered_refrigerators

@app.get("/refrigerators/{refrigerator_id}", response_model=Refrigerator)
def read_refrigerator(refrigerator_id: int):
    refrigerator = next((r for r in refrigerators if r.id == refrigerator_id), None)
    if refrigerator is None:
        raise HTTPException(status_code=404, detail="Refrigerator not found")
    return refrigerator

@app.post("/refrigerators/", response_model=Refrigerator)
def create_refrigerator(refrigerator: Refrigerator):
    if any(r.id == refrigerator.id for r in refrigerators):
        raise HTTPException(status_code=400, detail="Refrigerator ID already exists")
    refrigerators.append(refrigerator)
    return refrigerator

@app.put("/refrigerators/{refrigerator_id}", response_model=Refrigerator)
def update_refrigerator(refrigerator_id: int, refrigerator: Refrigerator):
    index = next((i for i, r in enumerate(refrigerators) if r.id == refrigerator_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Refrigerator not found")
    refrigerators[index] = refrigerator
    return refrigerator

@app.delete("/refrigerators/{refrigerator_id}", status_code=204)
def delete_refrigerator(refrigerator_id: int):
    index = next((i for i, r in enumerate(refrigerators) if r.id == refrigerator_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Refrigerator not found")
    refrigerators.pop(index)
    return None

