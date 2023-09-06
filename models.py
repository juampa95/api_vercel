from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, CheckConstraint, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base  = declarative_base()


class Medic(Base):
    __tablename__ = 'medicine'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40))
    drug = Column(String(40))
    concentration = Column(String(20))
    form = Column(String(20))
    gtin = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint('gtin >= 1000000000000', name='check_gtin_min_length'),
        CheckConstraint('gtin < 100000000000000', name='check_gtin_max_length')
    )


class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    personal_id = Column(Integer)
    name = Column(String(30))
    lastname = Column(String(20))
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint('personal_id >= 1000000000', name='check_DNI_min_length'),
        CheckConstraint('personal_id < 10000000000', name='check_DNI_max_length')
    )


class Prescriptions(Base):
    __tablename__ = 'medical_prescriptions'
    id = Column(Integer, primary_key=True)
    code = Column(String(20))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    patients = relationship('Patients')
    doctors = relationship('Doctor')



class Patients(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    personal_id = Column(Integer)
    name = Column(String(30))
    lastname = Column(String(20))
    date_of_birth = Column(Date)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint('personal_id >= 1000000000', name='check_DNI_min_length'),
        CheckConstraint('personal_id < 10000000000', name='check_DNI_max_length')
    )


class PrescriptionDetails(Base):
    __tablename__ = 'prescription_details'
    id = Column(Integer, primary_key=True)
    prescription_id = Column(Integer, ForeignKey('medical_prescriptions.id'))
    medicine_id = Column(Integer, ForeignKey('medicine.id'))
    qty = Column(Integer)

    medical_prescriptions = relationship('Prescriptions')
    medicine = relationship('Medic')


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    rating = Column(Float)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    author_id = Column(Integer, ForeignKey('author.id'))

    author = relationship('Author')


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

