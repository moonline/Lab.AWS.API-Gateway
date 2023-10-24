from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from controller.concert_controller import ConcertController
from repository.concert_repository import ConcertRepository


tracer = Tracer()
logger = Logger()

repository = ConcertRepository()
controller = ConcertController(repository)

router = APIGatewayHttpResolver()


@router.get('/concerts')
@tracer.capture_method
def get_concerts() -> list[dict]:
    """
    Example:
        curl --location 'https://{API_URL}/{STAGE}/concerts?artist={ARTIST}'
        e.g.
        curl --location 'https://nri2eiw521.execute-api.eu-central-1.amazonaws.com/dev/concerts?artist=Madonna'

    :return: A list of concerts. Example:
        [
            {
                "artist": "Madonna",
                "concert": "This is Madonna 2023",
                "ticket_sales": 5000000,
                "create_date": "2023-09-08T14:47:29.915661"
            },
            ...
        ]
    :rtype: list
    """
    parameters: dict = router.current_event.query_string_parameters

    return controller.get_concerts_action(parameters, {})


@router.put('/concerts')
@tracer.capture_method
def put_concert() -> dict:
    """
    Example:
        curl -X PUT --location 'https://{API_URL}/{STAGE}/concerts' \
            -H 'Content-Type: application/json' \
            -d '{ ... }'
        e.g.
        curl -X PUT --location 'https://vqi6qrgeai.execute-api.eu-central-1.amazonaws.com/dev/concerts' \
            -H 'Content-Type: application/json' \
            -d '{"artist":"Madonna","concert":"This is Madonna 2023","ticket_sales": 5000000}'

    :return: The created concert. Example:
        {
            "artist": "Madonna",
            "concert": "This is Madonna 2023",
            "ticket_sales": 5000000,
            "create_date": "2023-09-08T14:47:29.915661"
        }
    :rtype: dict
    """
    body: dict = router.current_event.json_body

    return controller.put_concert_action({}, body)


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
def handler(event: dict, context: LambdaContext) -> dict:
    """
    Powertools router

    :param event: An API Gateway event. Example:
        {
            ...
            'path': '/concerts',
            'httpMethod': 'GET',
            'queryStringParameters': {'artist': 'Madonna'},
            'requestContext': {},
            ...
        }
    :type event: dict

    :param context: Lambda context
    :type context: dict

    :rtype: json
    """
    return router.resolve(event, context)
