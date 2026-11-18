# Candidate ranking module strictly based on Random Forest predicted Hire probability


def calculate_candidate_score(candidate):
    # Extract the Random Forest predicted Hire probability as ranking score
    return candidate.get("hire_probability", 0.0)


def rank_candidates(candidates_list):
    # Rank candidates in descending order based strictly on predicted Hire probability
    if not candidates_list:
        return []

    # Sort descending by hire_probability
    ranked = sorted(
        candidates_list,
        key=lambda c: calculate_candidate_score(c),
        reverse=True,
    )

    # Assign 1-based ranking index
    for idx, cand in enumerate(ranked, start=1):
        cand["rank"] = idx

    return ranked

