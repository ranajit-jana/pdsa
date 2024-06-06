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
    entity_id: int

class RuleCreate(RuleBase):
    pass

class RuleUpdate(BaseModel):
    rule_description: str
    rule_category: str
    score: int
    entity_id: int

class Rule(RuleBase):
    rule_id: int

    class Config:
        orm_mode = True

class RuleGroupEntityMapBase(BaseModel):
    rule_id: int
    entity_id: int

class RuleGroupEntityMapCreate(RuleGroupEntityMapBase):
    map_id: int

class RuleGroupEntityMap(RuleGroupEntityMapBase):
    map_id: int

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
    record_id: int
    block_id: int
    case_id: int
    entity_id: int
    redacted_text: str

class PIIIdentificationRecordCreate(PIIIdentificationRecordBase):
    pass

class PIIIdentificationRecord(PIIIdentificationRecordBase):
    pir_id: int

    class Config:
        orm_mode = True

class BlockRuleScoreBase(BaseModel):
    case_id: int
    block_id: int
    score: int
    rules_match: List[int]

class BlockRuleScoreCreate(BlockRuleScoreBase):
    pass

class BlockRuleScore(BlockRuleScoreBase):
    bs_id: int

    class Config:
        orm_mode = True
