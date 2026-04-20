def classify(score):
    if score < 40:
        return "Weak"
    elif score < 70:
        return "Moderate"
    else:
        return "Practically Secure"