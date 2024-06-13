from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, crud, schemas
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

# CORS settings
origins = [
    "http://localhost:3000",  # React dev server
    # Add other origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to seed data
def seed_data():
    session = SessionLocal()

    # Define your seed data
    seed_entities = [
        models.PIIEntity(entity_name="PERSON", entity_description="Full name of the person", entity_category="Identity"),
        models.PIIEntity(entity_name="PHONE_NUMBER", entity_description="Contact phone number", entity_category="Identity"),
        models.PIIEntity(entity_name="EMAIL_ADDRESS", entity_description="Email address", entity_category="Identity"),
        models.PIIEntity(entity_name="AADHAAR", entity_description="Unique Identification Number of India", entity_category="Identity"),
        models.PIIEntity(entity_name="ADDRESS", entity_description="Residential address of Person", entity_category="Personal"),
        models.PIIEntity(entity_name="BANK_ACCOUNT", entity_description="Bank account number", entity_category="Financial"),
        models.PIIEntity(entity_name="CREDIT_CARD", entity_description="Credit card number", entity_category="Financial"),
        models.PIIEntity(entity_name="CREDIT_CARD_CVV", entity_description="Credit card CVV number", entity_category="Financial"),
        models.PIIEntity(entity_name="CREDIT_CARD_EXPIRY_DATE", entity_description="Credit card expiry date", entity_category="Financial"),
        models.PIIEntity(entity_name="DATE_OF_BIRTH", entity_description="Date of birth", entity_category="Personal"),
        models.PIIEntity(entity_name="MOTHERS_MAIDEN_NAME", entity_description="Mother's maiden name", entity_category="Personal"),
        models.PIIEntity(entity_name="PAN_NUMBER", entity_description="Permanent Account Number of Inda", entity_category="Identity")
    ]

    # Insert seed data into the session
    try:
        session.bulk_save_objects(seed_entities)
        session.commit()
    except IntegrityError:
        session.rollback()
        logger.info("Seed data already exists or there was an integrity error.")
    finally:
        session.close()

# Seed the data when the application starts
seed_data()


@app.post("/api/pii_entity/", response_model=schemas.PIIEntity)
def create_pii_entity(entity: schemas.PIIEntityCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received entity: {entity}")
        created_entity = crud.create_pii_entity(db, entity)
        logger.info(f"Created entity: {created_entity}")
        return created_entity
    except Exception as e:
        logger.exception("An error occurred during the PII entity creation")
        raise HTTPException(status_code=500, detail="An error occurred during the PII entity creation")

@app.get("/api/pii_entities/", response_model=list[schemas.PIIEntity])
def read_pii_entities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pii_entities = crud.get_pii_entities(db, skip=skip, limit=limit)
    return pii_entities

@app.put("/api/pii_entity/{entity_id}", response_model=schemas.PIIEntity)
def update_pii_entity(entity_id: int, entity: schemas.PIIEntityUpdate, db: Session = Depends(get_db)):
    db_entity = crud.update_pii_entity(db, entity_id, entity)
    if db_entity is None:
        raise HTTPException(status_code=404, detail="PIIEntity not found")
    return db_entity

@app.post("/api/rule/", response_model=schemas.Rule)
def create_rule(rule: schemas.RuleCreate, db: Session = Depends(get_db)):
    return crud.create_rule(db, rule)

@app.get("/api/rules/", response_model=list[schemas.Rule])
def read_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rules = crud.get_rules(db, skip=skip, limit=limit)
    return rules

@app.put("/api/rule/{rule_id}", response_model=schemas.Rule)
def update_rule(rule_id: int, rule: schemas.RuleUpdate, db: Session = Depends(get_db)):
    db_rule = crud.update_rule(db, rule_id, rule)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule

@app.get("/api/rule_group_entity_map", response_model=list[schemas.RuleGroupEntityMap])
def read_rule_group_entity_map(skip: int = 0, limit: int = 100, map: str = None, db: Session = Depends(get_db)):
    rule_group_entity_maps = crud.get_rule_group_entity_map(db, skip, limit, map)
    return rule_group_entity_maps

@app.post("/api/case")
def create_case(case: schemas.CaseCreate, db: Session = Depends(get_db)):
    return crud.create_case(db, case)

@app.get("/api/case", response_model=list[schemas.Case])
def read_case(skip: int = 0, limit: int = 100, map: str = None, db: Session = Depends(get_db)):
    cases = crud.get_cases(db, skip, limit, map)
    return cases

@app.post("/api/block")
def create_block(block: schemas.BlockCreate, db: Session = Depends(get_db)):
    return crud.create_block(db, block)

@app.get("/api/block", response_model=list[schemas.Block])
def read_block(skip: int = 0, limit: int = 100, map: str = None, db: Session = Depends(get_db)):
    blocks = crud.get_blocks(db, skip, limit, map)
    return blocks

@app.post("/api/pii_identification_record")
def create_pii_identification_record(record: schemas.PIIIdentificationRecordCreate, db: Session = Depends(get_db)):
    return crud.create_pii_identification_record(db, record)

@app.get("/api/pii_identification_record", response_model=list[schemas.PIIIdentificationRecord])
def read_pir(skip: int = 0, limit: int = 100, map: str = None, db: Session = Depends(get_db)):
    pirs = crud.get_pir(db, skip, limit, map)
    return pirs

@app.post("/api/block_rule_score", response_model=schemas.BlockRuleScoreCreate)
def create_block_rule_score(score: schemas.BlockRuleScoreCreate, db: Session = Depends(get_db)):
    logging.debug(f"Received request: {score}")
    try:
        db_score = crud.create_block_rule_score(db, score)
        return db_score
    except Exception as e:
        logging.error(f"Error creating block rule score: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api/block_rule_score", response_model=list[schemas.BlockRuleScore])
def read_brs(skip: int = 0, limit: int = 100, map: str = None, db: Session = Depends(get_db)):
    brs = crud.get_brs(db, skip, limit, map)
    return brs
