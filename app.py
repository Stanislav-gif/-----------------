from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Car(BaseModel):
    id: int
    make: str
    model: str
    year: int

cars = [Car(id=1, make="Toyota", model="Camry", year=2020),
        Car(id=2, make="BMW", model="X5", year=2021)]

@app.post("/cars/", response_model=Car)
def create_car(car: Car):
    if any(c.id == car.id for c in cars):
        raise HTTPException(status_code=400, detail="Car ID already exists")
    cars.append(car)
    return car

@app.get("/cars/{car_id}", response_model=Car)
def read_car(car_id: int):
    car = next((car for car in cars if car.id == car_id), None)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@app.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: int, car: Car):
    index = next((i for i, c in enumerate(cars) if c.id == car_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Car not found")
    cars[index] = car
    return car

@app.delete("/cars/{car_id}", status_code=204)
def delete_car(car_id: int):
    index = next((i for i, c in enumerate(cars) if c.id == car_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Car not found")
    cars.pop(index)
    return None

@app.get("/cars/", response_model=List[Car])
def read_cars(skip: int = 0, limit: int = 10):
    return cars[skip: skip + limit]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
