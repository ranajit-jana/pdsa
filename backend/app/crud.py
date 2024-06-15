from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from app import models
from app import schemas
import logging
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError

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
    db_rule = models.Rule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


def create_rule_and_mapping(db: Session, rule_data: dict, entity_ids: list):
    try:
        # Create new Rule
        new_rule = models.Rule(**rule_data)
        print(f" Rule as in create_rule_and_mapping {new_rule}")
        db.add(new_rule)
        db.commit()
        db.refresh(new_rule)

        # Add mappings
        for entity_id in entity_ids:
            new_mapping = models.RuleGroupEntityMap(
                rule_id=new_rule.rule_id, entity_id=entity_id
            )
            print(f"New mapping inside create_rule_and_mapping {new_rule.rule_id} {entity_id}")
            db.add(new_mapping)

        # Verify that mappings were added
        mappings = db.query(models.RuleGroupEntityMap).filter_by(rule_id=new_rule.rule_id).all()
        print(f"Mappings after commit: {mappings}")
        # Commit the transaction
        db.commit()
        db.refresh(new_rule)
        return {
            "rule_id": new_rule.rule_id,
            "rule_name": new_rule.rule_name,
            "rule_description": new_rule.rule_description,
            "rule_category": new_rule.rule_category,
            "score": new_rule.score,
            "entity_ids": entity_ids
        }

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def get_rules(db: Session, skip: int = 0, limit: int = 100):
    rules = db.query(models.Rule).offset(skip).limit(limit).all()
    print(f" The rules as returned {rules}")
    result = []
    for rule in rules:
        print(f" One rule at a time {rule.rule_id}")
        mappings = db.query(models.RuleGroupEntityMap).filter_by(rule_id=rule.rule_id).all()
        print(f"Mappings to be populated {mappings}")
        rule_with_mappings = schemas.RuleResponse(
            rule_id=rule.rule_id,
            rule_name=rule.rule_name,
            rule_description=rule.rule_description,
            rule_category=rule.rule_category,
            score=rule.score,
            entity_ids=[mapping.entity_id for mapping in mappings]
        )
        print(f"Entity list now {rule_with_mappings}")
        print(f"Entity list now {rule_with_mappings.entity_ids}")
        result.append(rule_with_mappings)
    return result

def update_rule(db: Session, rule_id: int, rule: schemas.RuleUpdate):
    db_rule = db.query(models.Rule).filter(models.Rule.rule_id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    # Update rule attributes
    if rule.rule_description:
        db_rule.rule_description = rule.rule_description
    if rule.rule_category:
        db_rule.rule_category = rule.rule_category
    if rule.score:
        db_rule.score = rule.score
    try:
        db.commit()
        db.refresh(db_rule)
        return db_rule
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(e))


def get_rule_group_entity_map(
    db: Session, skip: int = 0, limit: int = 100, map: str = None
):
    return db.query(models.RuleGroupEntityMap).offset(skip).limit(limit).all()


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
