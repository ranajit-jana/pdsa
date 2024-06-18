from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PIIEntityBase(BaseModel):
    entity_name: str
    entity_description: str
    entity_category: str


class PIIEntityCreate(PIIEntityBase):
    pass


class PIIEntityUpdate(BaseModel):
    entity_description: str
    entity_category: str


class PIIEntity(PIIEntityBase):
    entity_id: int

    class Config:
        orm_mode = True

class RuleBase(BaseModel):
    rule_name: str
    rule_description: str
    rule_category: str
    score: int
    entities: List[str]

class RuleCreate(RuleBase):
    pass

class RuleResponse(RuleBase):
    rule_id: int

    class Config:
        orm_mode = True


class RuleUpdate(BaseModel):
    rule_description: Optional[str] = None
    score: Optional[int] = None
    rule_category: Optional[str] = None
    entities: Optional[List[str]] = None

    class Config:
        orm_mode = True

class Rule(RuleBase):
    rule_id: int

    class Config:
        orm_mode = True

class RuleGroupEntityMapBase(BaseModel):
    rule_id: int
    entities: List[str]

class RuleGroupEntityMapCreate(RuleGroupEntityMapBase):
    map_id: int

class RuleGroupEntityMap(RuleGroupEntityMapBase):

    class Config:
        orm_mode = True

class CaseBase(BaseModel):
    case_name: str
    case_description: str
    start_time: datetime
    end_time: datetime


class CaseCreate(CaseBase):
    pass


class Case(CaseBase):
    case_id: int

    class Config:
        orm_mode = True


class BlockBase(BaseModel):
    block_name: str
    case_id: int
    source: str


class BlockCreate(BlockBase):
    pass


class Block(BlockBase):
    block_id: int

    class Config:
        orm_mode = True


class PIIIdentificationRecordBase(BaseModel):
    record_id: str
    block_hash: str
    case_hash: str
	case_name: str
    source: str
    entities_detected: List[str]
    redacted_text: str


class PIIIdentificationRecordCreate(PIIIdentificationRecordBase):
    pass

class PIIIdentificationRecordResponse(PIIIdentificationRecordBase):
    pir_id: int

    class Config:
        orm_mode = True


class BlockRuleScoreBase(BaseModel):
    case_hash: str
    block_hash: str
	case_name: str
    score: int
    rules_match: str
    source: str
	redacted_text: str

class BlockRuleScoreCreate(BlockRuleScoreBase):
    pass

class BlockRuleScore(BlockRuleScoreBase):
    bs_id: int

    class Config:
        orm_mode = True
