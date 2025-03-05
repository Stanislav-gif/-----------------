from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Phone(BaseModel):
    id: int
    model: str

phones: List[Phone] = [
        Phone(id=1, model="iPhone 13"),
        Phone(id=2, model="Samsung Galaxy S21"),
        Phone(id=3, model="Google Pixel 6")
]

@app.get("/phones/", response_model=List[Phone])
def read_phones(model: Optional[str] = None):
    if model:
        filtered_phones = []
        for phone in phones:
            if model.lower() in phone.model.lower():
                filtered_phones.append(phone)
        return filtered_phones
    else:
        return phones

@app.get("/phones/{phone_id}", response_model=Phone)
def read_phone(phone_id: int):
    phone = next((p for p in phones if p.id == phone_id), None)
    if phone is None:
        raise HTTPException(status_code=404, detail="Phone not found")
    return phone

@app.post("/phones/", response_model=Phone)
def create_phone(phone: Phone):
    if any(p.id == phone.id for p in phones):
        raise HTTPException(status_code=400, detail="Phone ID already exists")
    phones.append(phone)
    return phone

@app.put("/phones/{phone_id}", response_model=Phone)
def update_phone(phone_id: int, phone: Phone):
    index = next((i for i, p in enumerate(phones) if p.id == phone_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Phone not found")
    phones[index] = phone
    return phone

@app.delete("/phones/{phone_id}", status_code=204)
def delete_phone(phone_id: int):
    index = next((i for i, p in enumerate(phones) if p.id == phone_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Phone not found")
    phones.pop(index)
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
