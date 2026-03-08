# Policy Decision Point
# Bewertet eine Zugriffsanfrage anhand von Rolle und Zweckbindung

def evaluate_policy(
        role: str,
        requested_purpose: str,
        object_purpose: str,
        policy_version: str
        ):

    # Regel 1: Analyst darf nur auf Analytics-Daten für Analytics-Zwecke zugreifen
    if role == "analyst":
        
        # Zweck der Anfrage muss mit Zweck des Datenobjekt überein stimmen
        if requested_purpose == "analytics" and object_purpose == "analytics":

            return {
                "decision": "allow",
                "reason": "role_and_purpose_match",
                "policy_version": policy_version
            }

        # Zweck stimmt nicht überein -> Zugriff verweigern
        else:

            return {
                "decision": "deny",
                "reason": "purpose_mismatch",
                "policy_version": policy_version
            }

    # Regel 2: Support darf nur auf Support-Daten für Support-Zwecke zugreifen   
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
    
    # Regel 3: Gäste haben grundsätzlich keinen Zugriff
    elif role == "guest":

        return {
            "decision": "deny",
            "reason": "role_not_allowed",
            "policy_version": policy_version
        }
    
    # Default-Regel: unbekannte Rollen werden abgelehnt (deny-by-default)
    else:

        return {
            "decision": "deny",
            "reason": "role_not_allowed",
            "policy_version": policy_version
        }