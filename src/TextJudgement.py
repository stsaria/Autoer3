def true_false_string(text : str):
    text = text.lower()
    if text in ["true", "tru", "tr", "t"] or text in ["yes", "ye", "y"]:
        return True
    elif text.lower() in ["false", "fals", "fal", "fa", "f"] or text in ["no", "n"]:
        return False
    else:
        raise InterruptedError("The setting string can be `true`, `false` or `yes`, `no`")