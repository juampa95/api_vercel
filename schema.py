from pydantic import BaseModel
from datetime import date

class Medic(BaseModel):
    name: str
    drug: str
    concentration: str
    form: str
    gtin: str

    class Config:
        orm_mode = True


class Doctor(BaseModel):
    name: str
    lastname: str
    personal_id: str

    class Config:
        orm_mode = True


class Prescriptions(BaseModel):
    code: str
    patient_id: int
    doctor_id: int

    class Config:
        orm_mode = True


class Patients(BaseModel):
    name: str
    lastname: str
    personal_id: str
    date_of_birth: date

    class Config:
        orm_mode = True


class PrescriptionDetails(BaseModel):
    medicine_id: int
    qty: int

    class Config:
        orm_mode = True
