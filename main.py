import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy.exc import SQLAlchemyError

from models import Medic as ModelMedic
from models import Doctor as ModelDoctor
from models import Patients as ModelPatients
from models import Prescriptions as ModelPrescriptions
from models import PrescriptionDetails as ModelPDetails
from schema import Doctor as SchemaDoctor
from schema import Medic as SchemaMedic
from schema import Patients as SchemaPatients
from schema import Prescriptions as SchemaPrescriptions
from schema import PrescriptionDetails as SchemaPDetails


import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ['POSTGRES_URI'])


@app.get("/")
async def root():
    return {"message": "Server is up and running!"}

# Medicine

@app.get('/med/')
async def medics():
    medics = db.session.query(ModelMedic).all()
    return medics


@app.get('/med/{med_id}', response_model=SchemaMedic)
async def query_medics_by_id(med_id: int):
    db_medic = db.session.query(ModelMedic).filter_by(id=med_id).first()

    if db_medic is None:
        raise HTTPException(status_code=404, detail=f'Medic with ID {med_id} does not found')
    return db_medic


@app.post('/med/', response_model=SchemaMedic)
async def create_med(med: SchemaMedic):
    try:
        db_med = ModelMedic(name=med.name, drug=med.drug, concentration=med.concentration, form=med.form, gtin=med.gtin)
        db.session.add(db_med)
        db.session.commit()
        db.session.flush()
        return db_med

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error inserting into database: {str(e)}")
        return {"error": str(e)}


@app.delete('/med/{med_id}')
async def delete_med(med_id: int):
    try:
        db_med = db.session.query(ModelMedic).filter_by(id=med_id).first()
        if not db_med:
            raise HTTPException(status_code=404, detail="Medicine not found")

        db.session.delete(db_med)
        db.session.commit()
        db.session.refresh(db_med)
        return {'message': 'medicine deleted'}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

# Doctors

@app.get('/doc/')
async def doc():
    doc = db.session.query(ModelDoctor).all()
    return doc

@app.get('/doc/{doc_id}', response_model=SchemaDoctor)
async def query_doctor_by_id(doc_id: int):
    db_doc = db.session.query(ModelDoctor).filter_by(id=doc_id).first()
    if db_doc is None:
        raise HTTPException(status_code=404, detail=f'Doctor with ID {doc_id} does not found')
    return db_doc

@app.get('/doc/dni/{doc_dni}', response_model=SchemaDoctor)
async def query_doctor_by_id(doc_dni: str):
    db_doc = db.session.query(ModelDoctor).filter_by(personal_id=doc_dni).first()
    if db_doc is None:
        raise HTTPException(status_code=404, detail=f'Doctor with Personal ID {doc_dni} does not found')
    return db_doc

@app.post('/doc/', response_model=SchemaDoctor)
async def create_doc(doc: SchemaDoctor):
    try:
        db_doc = ModelDoctor(personal_id=doc.personal_id, name=doc.name, lastname=doc.lastname)
        db.session.add(db_doc)
        db.session.commit()
        db.session.flush()
        return db_doc

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error inserting into database: {str(e)}")
        return {"error": str(e)}

@app.delete('/doc/{doc_id}')
async def delete_doc(doc_id: int):
    try:
        db_doc = db.session.query(ModelDoctor).filter_by(id=doc_id).first()
        if not db_doc:
            raise HTTPException(status_code=404, detail="Medicine not found")

        db.session.delete(db_doc)
        db.session.commit()
        db.session.refresh(db_doc)
        return {'message': 'medicine deleted'}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

#Patients

@app.get('/patients/')
async def patients():
    p = db.session.query(ModelPatients).all()
    return p

@app.get('/patients/{p_id}', response_model=SchemaPatients)
async def query_patients_by_id(p_id: int):
    db_p = db.session.query(ModelPatients).filter_by(id=p_id).first()
    if db_p is None:
        raise HTTPException(status_code=404, detail=f'Patient with ID {db_p} does not found')
    return db_p

@app.post('/patients/', response_model=SchemaPatients)
async def create_patient(p: SchemaPatients):
    try:
        db_p = ModelPatients(name=p.name, lastname=p.lastname, personal_id=p.personal_id, date_of_birth=p.date_of_birth)
        db.session.add(p)
        db.session.commit()
        db.session.flush()
        return db_p
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error inserting into database: {str(e)}")
        return {"error": str(e)}


# DELETE

# PRESCRIPTION

@app.get('/pres/')
async def pres():
    prescriptions = db.session.query(ModelPrescriptions).all()
    return prescriptions

@app.get('/pres/{pres_id}', response_model=SchemaPatients)
async def query_pres_by_id(pres_id: int):
    db_pres = db.session.query(ModelPrescriptions).filter_by(id=pres_id).first()
    if not db_pres:
        raise HTTPException(status_code=404, detail=f'Prescription with ID {db_pres} does not found')
    return db_pres

@app.post('/pres/', response_model=SchemaPrescriptions)
async def create_pres(pres: SchemaPrescriptions):
    # verify that there is a doctor and a patient
    patient = db.session.query(ModelPatients).filter_by(id=pres.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail='Patient not found')
    doctor = db.session.query(ModelDoctor).filter_by(id=pres.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail='Doctor not found')

    try:
        db_pres = ModelPrescriptions(code=pres.code, patient_id=pres.patient_id, doctor_id=pres.doctor_id)
        db.session.add(db_pres)
        db.session.commit()
        db.session.flush()
        return db_pres
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error inserting into database: {str(e)}")
        return {"error": str(e)}


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)


