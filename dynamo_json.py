# This exists as a hack, but due to AWS's use of Decimals, it's probably permanent

import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def dumps(data) -> str:
    return json.dumps(data, cls=DecimalEncoder)