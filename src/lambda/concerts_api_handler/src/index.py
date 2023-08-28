from typing import Union

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.data_classes import (
    event_source,
    APIGatewayProxyEvent,
)

from controller.concerts_controller import ConcertsController
from repository.concerts_repository import ConcertsRepository


logger = Logger()
app = APIGatewayRestResolver()


@app.get('/concerts')
def get_concerts() -> list[dict]:
    """
    Example:
        curl --location 'https://{API_URL}/test/concerts?artist=Madonna'

    Returns:
        A list of concerts. Example:
        [
            {
                "artist": "Madonna",
                "concert": "This is Madonna 2023",
                "ticket_sales": 5000000
            },
            ...
        ]
    """
    parameters: dict = app.current_event.query_string_parameters

    repository = ConcertsRepository()
    controller = ConcertsController(repository)

    return controller.get_concerts_action(parameters)
    
    
@app.put('/concerts')
def put_concert() -> dict:
    """
    Example:
        curl --location 'https://{API_URL}/test/concerts?artist=Madonna'
            -H 'Content-Type: application/json' 
            -d '{"artist":"Madonna","concert":"This is Madonna 2023","ticket_sales": 5000000}'

    Returns:
        The created concert. Example:
        {
            "artist": "Madonna",
            "concert": "This is Madonna 2023",
            "ticket_sales": 5000000
        }
    """
    body: dict = app.current_event.json_body

    repository = ConcertsRepository()
    controller = ConcertsController(repository)

    return controller.put_concert_action(body)


@logger.inject_lambda_context
@event_source(data_class=APIGatewayProxyEvent)
def lambda_handler(event: dict, context: LambdaContext) -> Union[list, dict]:
    """
    App router for API Gateway event
    """
    return app.resolve(event, context)
