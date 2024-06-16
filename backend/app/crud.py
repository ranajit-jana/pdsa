from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from app import models
from app import schemas
import logging
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.models import RuleGroupEntityMap
from sqlalchemy import func

# Initialize logger
logger = logging.getLogger(__name__)


def create_pii_entity(db: Session, entity: schemas.PIIEntityCreate):
    db_entity = models.PIIEntity(**entity.dict())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def get_pii_entities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PIIEntity).offset(skip).limit(limit).all()


def update_pii_entity(db: Session, entity_id: int, entity: schemas.PIIEntityUpdate):
    db_entity = (
        db.query(models.PIIEntity)
        .filter(models.PIIEntity.entity_id == entity_id)
        .first()
    )
    if not db_entity:
        return None
    db_entity.entity_description = entity.entity_description
    db_entity.entity_category = entity.entity_category
    db.commit()
    db.refresh(db_entity)
    return db_entity



def create_rule(db: Session, rule: schemas.RuleCreate):
    db_rule = models.Rule(
        rule_name=rule.rule_name,
        rule_description=rule.rule_description,
        rule_category=rule.rule_category,
        score=rule.score,
        entities=rule.entities
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def get_rules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rule).offset(skip).limit(limit).all()

def update_rule(db: Session, rule_id: int, rule: schemas.RuleUpdate):
    db_rule = db.query(models.Rule).filter(models.Rule.rule_id == rule_id).first()
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    update_data = rule.dict(exclude_unset=True)
    
    # Ensure rule_name is not updated
    if "rule_name" in update_data:
        update_data.pop("rule_name")
    
    for key, value in update_data.items():
        setattr(db_rule, key, value)
    
    db.commit()
    db.refresh(db_rule)
    return db_rule

def get_rule_group_entity_map(db: Session, skip: int = 0, limit: int = 100, map: str = None):
    query = db.query(
        models.RuleGroupEntityMap.rule_id,
        func.array_agg(models.RuleGroupEntityMap.entities).label('entities')
    ).group_by(models.RuleGroupEntityMap.rule_id)
    
    if map:
        query = query.filter(models.RuleGroupEntityMap.rule_id == map)
    
    result = query.offset(skip).limit(limit).all()

    # Create a list of dictionaries with flattened entities
    rule_group_entity_maps = []
    for row in result:
        flattened_entities = [item for sublist in row.entities for item in sublist]
        rule_group_entity_maps.append({
            "rule_id": int(row.rule_id),  # Ensure rule_id is an integer
            "entities": flattened_entities  # Ensure entities is a list of strings
        })

    return rule_group_entity_maps

def create_case(db: Session, case: schemas.CaseCreate):
    db_case = models.Case(**case.dict())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case


def get_cases(db: Session, skip: int = 0, limit: int = 100, map: str = None):
    return db.query(models.Case).offset(skip).limit(limit).all()


def create_block(db: Session, block: schemas.BlockCreate):
    db_block = models.Block(**block.dict())
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block


def get_blocks(db: Session, skip: int = 0, limit: int = 100, map: str = None):
    return db.query(models.Block).offset(skip).limit(limit).all()


def create_pii_identification_record(
    db: Session, record: schemas.PIIIdentificationRecordCreate
):
    db_record = models.PIIIdentificationRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_pir(db: Session, skip: int = 0, limit: int = 100, map: str = None):
    return db.query(models.PIIIdentificationRecord).offset(skip).limit(limit).all()


def create_block_rule_score(db: Session, score: schemas.BlockRuleScoreCreate):
    db_score = models.BlockRuleScore(**score.dict())
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def get_brs(db: Session, skip: int = 0, limit: int = 100, map: str = None):
    return db.query(models.BlockRuleScore).offset(skip).limit(limit).all()

