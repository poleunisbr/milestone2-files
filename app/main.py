from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Define FastAPI app
app = FastAPI()

# CORS (Cross-Origin Resource Sharing) Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with the specific origin of your frontend app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define SQLAlchemy models
Base = declarative_base()

class Item(Base):
    __tablename__ = "name"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Create PostgreSQL database engine
DATABASE_URL = "postgresql://bryan:pass@192.168.1.176:5432/name"
engine = create_engine(DATABASE_URL)

# Define SessionLocal using sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Create Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# New API endpoint to get the name from the database
@app.get("/name", response_model=dict)
def get_name(db: Session = Depends(get_db)):
    name = db.query(Item.name).first()
    if not name:
        raise HTTPException(status_code=404, detail="Name not found")
    return {"name": name}
