def getNumberString(number: int):
    if str(number).endswith("1") and len(str(number)) == 1:
        x = str(number) + "st"
    elif str(number).endswith("2"):
        x = str(number) + "nd"
    elif str(number).endswith("3"):
        x = str(number) + "rd"
    elif str(number).endswith("11") and len(str(number)) == 2:
        x = str(number) + "th"
    else:
        x = str(number) + "th"
    return x
