from app import models, crud


def match_rules(entities_detected, rules):
    """
    Check if the provided entities detected match the rule entities.
    """
    print(f" The entities detected {entities_detected}")
    detected_entities_set = set(entities_detected)
    matched_rules = []

    for rule in rules:
        rule_entities_set = set(rule.entities)

        # Check if the detected entities include all entities in the rule
        if detected_entities_set.issuperset(rule_entities_set):
            matched_rules.append(rule)

    # Filter out smaller sets if a larger set matches
    if matched_rules:
        max_entities_count = max(len(set(rule.entities)) for rule in matched_rules)
        best_matches = [rule for rule in matched_rules if len(set(rule.entities)) == max_entities_count]
        
        # If there is more than one distinct match with the same size, return all of them
        distinct_best_matches = []
        for match in best_matches:
            if not any(set(other.entities).issuperset(set(match.entities)) and set(other.entities) != set(match.entities) for other in best_matches):
                distinct_best_matches.append(match)

        return distinct_best_matches

    return matched_rules


def score_processing(db, db_record):
    """
    Process the score calculation and update the block_rule_score table.
    """
    entities_detected = db_record.entities_detected

    # Fetch rules from the database
    rules = crud.get_rules(db)

    # Placeholder for formatted matched rule names
    matched_rule_names = []

    # Find the best matching rules
    best_match_rules = match_rules(entities_detected, rules)
    matched_rule_names = [rule.rule_name for rule in best_match_rules] if best_match_rules else []
    highest_score = max(rule.score for rule in best_match_rules) if best_match_rules else 0

    # Insert into block_rule_score table
    block_rule_score = models.BlockRuleScore(
        block_hash=db_record.block_hash,
        case_name=db_record.case_name,
        case_hash=db_record.case_hash,
        source=db_record.source,
        redacted_text=db_record.redacted_text,
        score=highest_score,
        rules_match=matched_rule_names,
    )
    db.add(block_rule_score)
    db.commit()

    print("Updated Block Score successfully")
