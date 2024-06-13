
API Call with the payload as below.
```


{ "Job_run": "case_id", # cron Job number (can be epoch time) "record_id": "document_id" # text which is analysed “source”: “C:/folder/sometextwithPII.pdf” # source of text,DB or File "block_id" : "Hash", # metadata hash identifies the source of text "entities_detected": [ "PERSON", "DOB", "MOTHER_NAME", "CREDIT_CARD" ], "redacted_text" : { "Free-flowing text with redacted PII" } }



{ "Job_run": "1", ,"record_id": "1" , “source”: “C:/folder/sometextwithPII.pdf", "block_id" : "1", "entities_detected": [ "PERSON", "DOB", "MOTHER_NAME", "CREDIT_CARD" ], "redacted_text" : { "Free-flowing text with redacted PII" } }

{ "Job_run": "1", ,"record_id": "2" , “source”: “C:/folder/sometextwithPII.pdf", "block_id" : "1", "entities_detected": [ "DOB", "MOTHER_NAME", "CREDIT_CARD" ], "redacted_text" : { "Free-flowing text with redacted PII" } }

```


This API call populate the table if the trigger is not end call. ( good to have is validate the entity is correct of not example POERSON may not be able to map to PERSON)

class PIIIdentificationRecord(Base):
    __tablename__ = "pii_identification_record"
    pir_id = Column(Integer, primary_key=True, autoincrement=True)
    source = 
    record_id = Column(Integer, nullable=False)
    block_id = Column(Integer, nullable=False)
    case_id = Column(Integer, nullable=False)
    entities_detected = Column(ARRAY(String), nullable=False)  # Define as ARRAY of Integer
    redacted_text = Column(String, nullable=False)



Example

Case 1
Block 1
Record 1 
ENTITIES Detected : PERSON


Case 1
Block 1
Record 2
ENTITIES Detected : PERSON, DOB

Case 1
Block 1 (Hash)
Record 2
ENTITIES Detected : MOTHER_NAME, CREDIT_CARD


Next the block closure call comes.

```
{ "Job_run": "case_id", 
# cron Job number (can be epoch time) 
"record_id": "document_id" # text which is analysed 
“source”: “C:/folder/sometextwithPII.pdf” # source of text,DB or File 
"block_id" : "Hash", 

# metadata hash identifies the source of text 

"ending_block": yes, 
 }
```

for block 1 we will query the above table and get all the entities in a list .

actual for block 1 will be (PERSON, PERSON,DOB, MOTHER_NAME, CREDIT_CARD) but  
set with unique elements will be ( PERSON,DOB, MOTHER_NAME, CREDIT_CARD)

That will be (PERSON,DOB, MOTHER_NAME, CREDIT_CARD) This need to be super set 
Rule is

now if we match it with rules. 

All the rules needs to be loaded in memory 

Rule 1 - ( PERSON, DOB, MOTHER_NAME) match against (PERSON, CREDIT_CARD, DOB, MOTHER_NAME) - Match = True 
RULE 2 - (PERSON, CREDIT_CARD) match against (PERSON,DOB, MOTHER_NAME, CREDIT_CARD) = Match = True
Rule 3- (PERSON, CREDIT_CARD, CREDIT_CARD_CVV, CREDIT_CARD_EXP_DATE ) Match against (PERSON,DOB, MOTHER_NAME, CREDIT_CARD)  Match = False

If match is true we will populate the following table

class BlockRuleScore(Base):
    __tablename__ = "block_rule_score"
    bs_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    block_id = Column(Integer, ForeignKey("block.block_id"))

    source =
    score = Column(Integer)
    rules_match = Column(Integer, ForeignKey("rules.rule_id"))


Example 2  - To be implemented later.


That will be (PERSON,DOB, MOTHER_NAME, CREDIT_CARD, CREDIT_CARD_CVV, CREDIT_CARD_EXP_DATE)

now if we match it with rules. 

All the rules needs to be loaded in memory 

Rule 1 - ( PERSON, DOB, MOTHER_NAME) match against (PERSON,DOB, MOTHER_NAME, CREDIT_CARD, CREDIT_CARD_CVV, CREDIT_CARD_EXP_DATE)) - Match = True Score 5
RULE 2 - (PERSON, CREDIT_CARD) match against (PPERSON,DOB, MOTHER_NAME, CREDIT_CARD, CREDIT_CARD_CVV, CREDIT_CARD_EXP_DATE) = Match = True       Score 6
Rule 3-  (PERSON, CREDIT_CARD, CREDIT_CARD_CVV, CREDIT_CARD_EXP_DATE ) Match against (PERSON,DOB, MOTHER_NAME, CREDIT_CARD, CREDIT_CARD_CVV, CREDIT_CARD_EXP_DATE)  Match = True                                                                                                              Score 10


Rule 2 is subset of Rule 3 ( then i will take rule 3 only, and ignore rule 2)

Rule 2 is subset of rule 3 we need to consider rule 2


