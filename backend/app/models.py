from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.dialects.postgresql import ARRAY

class PIIEntity(Base):
    __tablename__ = "pii_entities"
    entity_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entity_name = Column(String, unique=True, index=True)
    entity_description = Column(String)
    entity_category = Column(String)


class Rule(Base):
    __tablename__ = 'rules'
    rule_id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String)
    rule_description = Column(String)
    score = Column(Integer)
    rule_category = Column(String)
    entities = Column(ARRAY(String))

class RuleGroupEntityMap(Base):
    __tablename__ = "rule_group_entity_map"
    map_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rule_id = Column(Integer, ForeignKey("rules.rule_id"))
    entities = Column(ARRAY(String))

class Case(Base):
    __tablename__ = "cases"
    case_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    case_name = Column(String, index=True)
    case_description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)


class Block(Base):
    __tablename__ = "block"
    block_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    block_name = Column(String, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    source = Column(String)


class PIIIdentificationRecord(Base):
    __tablename__ = "pii_identification_record"
    pir_id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(String, nullable=False)
    block_hash = Column(String, nullable=False)
    case_hash = Column(String, nullable=False)
    case_name = Column(String, nullable=False)
    source = Column(String, nullable=False)
    entities_detected = Column(ARRAY(String), nullable=False)
    redacted_text = Column(String, nullable=False)

class BlockRuleScore(Base):
    __tablename__ = "block_rule_score"
    bs_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    block_hash = Column(String, nullable=False)
    case_name = Column(String, nullable=False)
    case_hash = Column(String, nullable=False)
    source = Column(String, nullable=False)
    redacted_text = Column(String)
    score = Column(Integer)
    rules_match = Column(String, nullable=False)