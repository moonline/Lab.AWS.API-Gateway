from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from controller.concerts_controller import ConcertsController
from repository.concerts_repository import ConcertsRepository


tracer = Tracer()
logger = Logger()
app = APIGatewayHttpResolver()

@app.get('/concerts')
@tracer.capture_method
def get_concerts() -> list[dict]:
    """
    Example:
        curl --location 'https://{API_URL}/{STAGE}/concerts?artist=Madonna'
        e.g.
        curl --location 'https://nri2eiw521.execute-api.eu-central-1.amazonaws.com/dev/concerts?artist=Madonna'

    :return: A list of concerts. Example:
        [
            {
                "artist": "Madonna",
                "concert": "This is Madonna 2023",
                "ticket_sales": 5000000,
                "created_date": "2023-09-08T14:47:29.915661"
            },
            ...
        ]
    """
    parameters: dict = app.current_event.query_string_parameters

    repository = ConcertsRepository()
    controller = ConcertsController(repository)

    return controller.get_concerts_action(parameters)


@app.put('/concerts')
@tracer.capture_method
def put_concert() -> dict:
    """
    Example:
        curl -X PUT --location 'https://vqi6qrgeai.execute-api.eu-central-1.amazonaws.com/dev/concerts' \
            -H 'Content-Type: application/json' \
            -d '{"artist":"Madonna","concert":"This is Madonna 2023","ticket_sales": 5000000}'

    :return: The created concert. Example:
        {
            "artist": "Madonna",
            "concert": "This is Madonna 2023",
            "ticket_sales": 5000000,
            "created_date": "2023-09-08T14:47:29.915661"
        }
    """
    body: dict = app.current_event.json_body

    repository = ConcertsRepository()
    controller = ConcertsController(repository)

    return controller.put_concert_action(body)


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
