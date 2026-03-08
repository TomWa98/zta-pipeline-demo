def evaluate_policy(
        role: str,
        requested_purpose: str,
        object_purpose: str,
        policy_version: str
        ):

    if role == "analyst":

        if requested_purpose == "analytics" and object_purpose == "analytics":

            return {
                "decision": "allow",
                "reason": "role_and_purpose_match",
                "policy_version": policy_version
            }

        else:

            return {
                "decision": "deny",
                "reason": "purpose_mismatch",
                "policy_version": policy_version
            }
        
    elif role == "support":

        if requested_purpose == "support" and object_purpose == "support":

            return {
                "decision": "allow",
                "reason": "role_and_purpose_match",
                "policy_version": policy_version
            }
        
        else:

            return {
                "decision": "deny",
                "reason": "purpose_mismatch",
                "policy_version": policy_version
            }
    
    elif role == "guest":

        return {
            "decision": "deny",
            "reason": "role_not_allowed",
            "policy_version": policy_version
        }
    
    else:

        return {
            "decision": "deny",
            "reason": "role_not_allowed",
            "policy_version": policy_version
        }