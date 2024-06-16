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
    entity_ids: List[str]

class RuleCreate(RuleBase):
    pass

class RuleResponse(RuleBase):
    rule_id: int

    class Config:
        orm_mode = True


class RuleUpdate(BaseModel):
    rule_name: Optional[str] = None
    rule_description: Optional[str] = None
    rule_category: Optional[str] = None
    score: Optional[int] = None
    entity_ids: Optional[List[str]] = None


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
    block_id: str
    case_id: str
    source: str
    entity_name: List[str]
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
    rules_match: int


class BlockRuleScoreCreate(BlockRuleScoreBase):
    pass


class BlockRuleScore(BlockRuleScoreBase):
    bs_id: int

    class Config:
        orm_mode = True
