from fastapi import FastAPI
from app.routers import booking, company, equipment, maintenance
from app.databases.database import Base, engine
from app.routers import user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(maintenance.router)
app.include_router(equipment.router)
app.include_router(booking.router)
app.include_router(company.router)