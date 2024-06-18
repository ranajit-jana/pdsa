import asyncio


async def score_processing(db_record):


    # Entities detected from the record
    entities_detected = db_record.entities_detected

    # 2. Fetch rules from the database
    rules = crud.get_rules(db)

    # Placeholder for formatted matched rule names
    formatted_matched_rules = []

    # 3. Perform rules matching logic
    for rule in rules:
        if match_rule(entities_detected, rule.entities):
            # Format the rule name as desired
            formatted_rule_name = rule.rule_name.replace('_', ' ')
            formatted_matched_rules.append(formatted_rule_name)

    # Join formatted matched rule names into a single string
    joined_matched_rules = ", ".join(formatted_matched_rules)

    # 4. Insert into block_rule_score table
    block_rule_score = models.BlockRuleScore(
        block_hash=record.block_hash,
        case_hash=record.case_hash,
        source=record.source,
        score=len(entities_detected),
        rules_match=joined_matched_rules
    )
    db.add(block_rule_score)
    db.commit()

    print("Updated Block Score successfully")
