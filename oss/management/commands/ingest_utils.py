def test_qs_unique_result(qs, search_terms):
    """Function to check that a query returned a unique result"""

    if len(qs) == 1:
        message = 'OK'
        object = qs[0]

    elif len(qs) > 1:
        message = 'Warning: ambiguous search criteria '+' '.join(search_terms)
        object = None

    else:
        message = 'Warning: unrecognised search criteria '+' '.join(search_terms)
        object = None

    return object, message
