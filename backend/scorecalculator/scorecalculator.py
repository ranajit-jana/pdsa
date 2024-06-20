from app import models, crud

def match_rule(entities_detected, rule_entities):
    """
    Check if the provided entities detected match the rule entities.
    """
    return set(entities_detected).issuperset(set(rule_entities))

def score_processing(db, db_record):
    """
    Process the score calculation and update the block_rule_score table.
    """
    entities_detected = db_record.entities_detected

    # Fetch rules from the database
    rules = crud.get_rules(db)

    # Placeholder for formatted matched rule names
    matched_rule_names = []

    # Perform rules matching logic
    for rule in rules:
        if match_rule(entities_detected, rule.entities):
            matched_rule_names.append(rule.rule_name)

    # Insert into block_rule_score table
    block_rule_score = models.BlockRuleScore(
        block_hash=db_record.block_hash,
        case_name=db_record.case_name,
        case_hash=db_record.case_hash,
        source=db_record.source,
        redacted_text=db_record.redacted_text,
        score=len(entities_detected),
        rules_match=matched_rule_names
    )
    db.add(block_rule_score)
    db.commit()

    print("Updated Block Score successfully")
