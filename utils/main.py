from walker.log import RECORD_TYPE


def get_token_type(val):
    return val["token_type"]


def create_token(tokenType, value=None):
    token = {"token_type": tokenType}
    if value is not None:
        token["value"] = value
    return token


def convert_log_list_into_dict_list(log):
    output = []
    for entry in log:
        if entry[0] == RECORD_TYPE.COMMAND:
            output.append(
                {
                    "recordType": str(entry[0]),
                    "commandType": str(entry[1]),
                    "varType": str(entry[2]),
                    "var": entry[3],
                    "value": entry[4],
                    "index": entry[5],
                }
            )
        else:
            output.append(
                {
                    "recordType": str(entry[0]),
                    "hintType": str(entry[1]),
                    "target": entry[2],
                    "values": entry[3],
                }
            )
    return output
