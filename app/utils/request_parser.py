def parse_request(request):
    """ Parse and validate Vectorizer Request
    Arguments:
       [flask.request] -- [flask request for vectorisation]
    Returns:
        [None/dict,flask.request] -- [(errors if any),flask request]
    """

    error = None

    # validating the request json to be a list and to have both the required keys for vectorisation
    if isinstance(request.json, list) and all([list(element.keys()) == ['text', 'image'] for element in request.json]):
        pass
    else:
        error = {'error': 'Invalid Request'}
    return error, request
