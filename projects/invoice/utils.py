def to_persian_number(value):

    if value is None:
        return ""

    value = "{:,.0f}".format(float(value))

    english = "0123456789,"
    persian = "۰۱۲۳۴۵۶۷۸۹٬"

    table = str.maketrans(english, persian)

    return value.translate(table)


def to_persian_text(text):

    if text is None:
        return ""

    english = "0123456789"
    persian = "۰۱۲۳۴۵۶۷۸۹"

    table = str.maketrans(english, persian)

    return str(text).translate(table)