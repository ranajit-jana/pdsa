from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base

class PIIEntity(Base):
    __tablename__ = "pii_entities"
    entity_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entity_name = Column(String, index=True)
    entity_description = Column(String)
    entity_category = Column(String)

class Rule(Base):
    __tablename__ = "rules"
    rule_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rule_name = Column(String, index=True)
    rule_description = Column(String)
    rule_category = Column(String)  # Add this line
    score = Column(Integer)
    entity_id = Column(Integer, ForeignKey("pii_entities.entity_id"))

class RuleGroupEntityMap(Base):
    __tablename__ = "rule_group_entity_map"
    map_id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey("rules.rule_id"))
    entity_id = Column(Integer, ForeignKey("rules.entity_id"))

class Case(Base):
    __tablename__ = "cases"
    case_id = Column(Integer, primary_key=True, index=True)
    case_name = Column(String, index=True)
    case_description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

class Block(Base):
    __tablename__ = "block"
    block_id = Column(Integer, primary_key=True, index=True)
    block_name = Column(String, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    source = Column(String)

class PIIIdentificationRecord(Base):
    __tablename__ = "pii_identification_record"
    pir_id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer)
    block_id = Column(Integer, ForeignKey("block.block_id"))
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    entity_id = Column(Integer, ForeignKey("pii_entities.entity_id"))
    redacted_text = Column(String)

class BlockRuleScore(Base):
    __tablename__ = "block_rule_score"
    bs_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    block_id = Column(Integer, ForeignKey("block.block_id"))
    score = Column(Integer)
    rules_match = Column(ARRAY(Integer))
