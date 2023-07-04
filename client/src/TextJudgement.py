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

def inside_text(text : str):
    if text in ['',' ']:
        return False
    else:
        return True