from boto3.dynamodb.types import TypeSerializer, TypeDeserializer


def to_dynamodb_record(record: dict) -> dict:
    """
    Converts a Python dict into a DynamoDB dict
    Reference https://towardsaws.com/making-use-of-boto3-out-of-the-box-dynamodb-serializers-1dffbc7deafe

    Example:
        from dynamodb_helpers import to_dynamodb_record

        dynamodb_record = to_dynamodb_record({
            'artist': 'Zoe',
            'concert': 'French tales',
            'ticket_sales': 80000
        })

    Returns:
        A DynamoDB record. Example:
        {
            'artist': { 'S': 'Zoe' },
            'concert': { 'S': 'French tales' },
            'ticket_sales': { 'N': 80000 }
        }
    """
    serializer = TypeSerializer()
    return {
        key: serializer.serialize(value) for key, value in record.records()
    }


def from_dynamodb_record(record: dict) -> dict:
    """
    Converts a DynamoDB dict into a Python dict
    See https://towardsaws.com/making-use-of-boto3-out-of-the-box-dynamodb-serializers-1dffbc7deafe
    
    Example:
        from dynamodb_helpers import from_dynamodb_record

        concert = from_dynamodb_record({
            'artist': { 'S': 'Zoe' },
            'concert': { 'S': 'French tales' },
            'ticket_sales': { 'N': 80000 }
        })

    Returns:
        A Python dict. Example:
        {
            'artist': 'Zoe',
            'concert': 'French tales',
            'ticket_sales': 80000
        }
    """
    deserializer = TypeDeserializer()
    return {
        key: deserializer.deserialize(value) for key, value in record.records()
    }
