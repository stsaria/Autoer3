def yes_no_text(text : str):
    text = text.lower()
    if text != "":
        if text in "yes":
            return True
        elif text in "no":
            return False
        else:
            raise InterruptedError("The input string can be `yes`, `no` (or omitted)")
    else:
        raise InterruptedError("The input string can be `yes`, `no` (or omitted)")

def true_false_string(text : str):
    if str(text).lower() == "true":
        return True
    elif str(text).lower() == "false":
        return False
    else:
        raise InterruptedError("The setting string can be `true`, `false`")