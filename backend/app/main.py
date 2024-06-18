from typing import List
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, APIRouter
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, crud, schemas
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from scorecalculator.scorecalculator import score_processing

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
        models.PIIEntity(
            entity_name="PERSON",
            entity_description="Full name of the person",
            entity_category="Identity",
        ),
        models.PIIEntity(
            entity_name="PHONE_NUMBER",
            entity_description="Contact phone number",
            entity_category="Identity",
        ),
        models.PIIEntity(
            entity_name="EMAIL_ADDRESS",
            entity_description="Email address",
            entity_category="Identity",
        ),
        models.PIIEntity(
            entity_name="AADHAAR",
            entity_description="Unique Identification Number of India",
            entity_category="Identity",
        ),
        models.PIIEntity(
            entity_name="ADDRESS",
            entity_description="Residential address of Person",
            entity_category="Personal",
        ),
        models.PIIEntity(
            entity_name="BANK_ACCOUNT",
            entity_description="Bank account number",
            entity_category="Financial",
        ),
        models.PIIEntity(
            entity_name="CREDIT_CARD",
            entity_description="Credit card number",
            entity_category="Financial",
        ),
        models.PIIEntity(
            entity_name="CREDIT_CARD_CVV",
            entity_description="Credit card CVV number",
            entity_category="Financial",
        ),
        models.PIIEntity(
            entity_name="CREDIT_CARD_EXPIRY_DATE",
            entity_description="Credit card expiry date",
            entity_category="Financial",
        ),
        models.PIIEntity(
            entity_name="DATE_OF_BIRTH",
            entity_description="Date of birth",
            entity_category="Personal",
        ),
        models.PIIEntity(
            entity_name="MOTHERS_MAIDEN_NAME",
            entity_description="Mother's maiden name",
            entity_category="Personal",
        ),
        models.PIIEntity(
            entity_name="PAN_NUMBER",
            entity_description="Permanent Account Number of India",
            entity_category="Identity",
        ),
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
        raise HTTPException(
            status_code=500, detail="An error occurred during the PII entity creation"
        )


@app.get("/api/pii_entities/", response_model=List[schemas.PIIEntity])
def read_pii_entities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pii_entities = crud.get_pii_entities(db, skip=skip, limit=limit)
    return pii_entities


@app.put("/api/pii_entity/{entity_id}", response_model=schemas.PIIEntity)
def update_pii_entity(
    entity_id: int, entity: schemas.PIIEntityUpdate, db: Session = Depends(get_db)
):
    db_entity = crud.update_pii_entity(db, entity_id, entity)
    if db_entity is None:
        raise HTTPException(status_code=404, detail="PIIEntity not found")
    return db_entity


@app.post("/api/rule", response_model=schemas.RuleResponse)
def create_rule(rule: schemas.RuleCreate, db: Session = Depends(get_db)):
    print(f"Received rule: %s", rule.dict())
    try:
        created_rule = crud.create_rule(db=db, rule=rule)
        logger.debug("Created rule: %s", created_rule)
        return created_rule
    except Exception as e:
        logger.error("Error creating rule: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/api/rules/", response_model=List[schemas.Rule])
def read_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rules = crud.get_rules(db, skip=skip, limit=limit)
    return rules

@app.put("/api/rule/{rule_id}", response_model=schemas.RuleResponse)
def update_rule(rule_id: int, rule: schemas.RuleUpdate, db: Session = Depends(get_db)):
    print(f"Received rule: {rule.dict()}")
    print(f" The ID passed is {rule_id}")
    return crud.update_rule(db=db, rule_id=rule_id, rule=rule)

@app.get("/api/rule_group_entity_map", response_model=List[schemas.RuleGroupEntityMap])
def read_rule_group_entity_map(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rule_group_entity_maps = crud.get_rule_group_entity_map(db, skip=skip, limit=limit)
    return rule_group_entity_maps

@app.post("/api/case", response_model=schemas.Case)
def create_case(case: schemas.CaseCreate, db: Session = Depends(get_db)):
    return crud.create_case(db, case)

@app.get("/api/case", response_model=List[schemas.Case])
def read_case(skip: int = 0, limit: int = 100, map: str = None, db: Session = Depends(get_db)):
    cases = crud.get_cases(db, skip, limit, map)
    return cases

@app.post("/api/block", response_model=schemas.Block)
def create_block(block: schemas.BlockCreate, db: Session = Depends(get_db)):
    return crud.create_block(db, block)

@app.get("/api/block", response_model=List[schemas.Block])
def read_block(skip: int = 0, limit: int = 100, map: str = None, db: Session = Depends(get_db)):
    blocks = crud.get_blocks(db, skip, limit, map)
    return blocks

# Initialize router
router = APIRouter()

@app.get("/api/pii_identification_record", response_model=List[schemas.PIIIdentificationRecordBase])
def read_pir(skip: int = 0, limit: int = 100, map: str = None, db: Session = Depends(get_db)):
    pirs = crud.get_pir(db, skip, limit, map)
    return pirs

def match_rule(entities_detected, rule_entities):
    """
    Check if the provided entities detected match the rule entities.
    """
    return set(entities_detected).issuperset(set(rule_entities))


@app.post("/api/pii_identification_record")
def create_pii_identification_record(
    record: schemas.PIIIdentificationRecordCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None,
):
    try:
        print({key: record.dict()[key] for key in ["source", "entity_name"]})
        db_record = crud.create_pii_identification_record(db, record)
        background_tasks.add_task(score_processing, db_record)
        return db_record

    except ValidationError as e:
        print(e.json())  # Print validation errors
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/block_rule_score", response_model=schemas.BlockRuleScoreCreate)
def create_block_rule_score(
    score: schemas.BlockRuleScoreCreate, db: Session = Depends(get_db)
):
    logging.debug(f"Received request: {score}")
    try:
        db_score = crud.create_block_rule_score(db, score)
        return db_score
    except Exception as e:
        logging.error(f"Error creating block rule score: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api/block_rule_score", response_model=List[schemas.BlockRuleScore])
def read_brs(skip: int = 0, limit: int = 100, map: str = None, db: Session = Depends(get_db)):
    brs = crud.get_brs(db, skip, limit, map)
    return brs

# Include the router in the FastAPI app
app.include_router(router, prefix="/api")
