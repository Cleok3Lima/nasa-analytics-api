from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

DATABASE_URL = "postgresql://user:password@db/nasa_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ApiUsage(Base):
    __tablename__ = "api_usage"
    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

@app.post("/track")
def track_usage():
    db = SessionLocal()
    usage = db.query(ApiUsage).first()
    if not usage:
        usage = ApiUsage(count=1)
    else:
        usage.count += 1
    db.add(usage)
    db.commit()
    db.close()
    return {"message": "Uso registrado"}

@app.get("/stats")
def get_stats():
    db = SessionLocal()
    usage = db.query(ApiUsage).first()
    db.close()
    return {"total_requests": usage.count if usage else 0}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
