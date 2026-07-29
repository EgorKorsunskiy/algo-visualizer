from walker.log import RECORD_TYPE


def getTokenType(val):
    return val["token_type"]


def createToken(tokenType, value=None):
    token = {"token_type": tokenType}
    if value is not None:
        token["value"] = value
    return token


def convertLogListIntoDictList(log):
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
