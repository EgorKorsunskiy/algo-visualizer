def get_token_type(val):
    return val["token_type"]


def create_token(tokenType, value=None):
    token = {"token_type": tokenType}
    if value is not None:
        token["value"] = value
    return token
