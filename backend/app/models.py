from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base


class PIIEntity(Base):
    __tablename__ = "pii_entities"
    entity_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entity_name = Column(String, unique=True, index=True)
    entity_description = Column(String)
    entity_category = Column(String)


class Rule(Base):
    __tablename__ = "rules"
    rule_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rule_name = Column(String, index=True)
    rule_description = Column(String)
    rule_category = Column(String)  # Add this line
    score = Column(Integer)
    entity_ids= Column(ARRAY(Integer), nullable=False)



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
    block_id = Column(String, nullable=False)
    case_id = Column(String, nullable=False)
    source = Column(String, nullable=False)
    entity_name = Column(ARRAY(String), nullable=False)  # Define as ARRAY of string
    redacted_text = Column(String)


class BlockRuleScore(Base):
    __tablename__ = "block_rule_score"
    bs_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    block_id = Column(Integer, ForeignKey("block.block_id"))
    score = Column(Integer)
    rules_match = Column(Integer, ForeignKey("rules.rule_id"))
