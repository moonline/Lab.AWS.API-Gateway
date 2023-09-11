from __future__ import annotations
import os
import re

from aws_lambda_powertools.event_handler.exceptions import BadRequestError

from model.concert import Concert
from repository.concerts_repository import ConcertsRepository
from controller.concerts_validator import validate_get_concerts_event, validate_put_concert_event


class ConcertsController:
    def __init__(self, repository: ConcertsRepository) -> ConcertsController:
        """
        Example:
            from repository.concerts_repository import ConcertsRepository
            from controller.concerts_controller import ConcertsController
            
            repository = ConcertsRepository()
            controller = ConcertsController(repository)

        :return: A ConcertsController instance
        """
        self.repository = repository

    def get_concerts_action(self, parameters: dict, body: dict) -> list[Concert]:
        """
        Example:
            controller.get_concerts_action(
                { "artist": "Madonna" }
            )

        :param dict parameters: API GW parameters. Example:
            { "artist": "Madonna" }

        :return: A list of concerts matching the parameters. Example:
            [
                {
                    "artist": "Madonna",
                    "concert": "This is Madonna 2023",
                    "ticket_sales": 5000000,
                    "created_date": "2023-09-08T14:47:29.915661"
                },
                ...
            ]

        :raises BadRequestError: For validation errors. Example:
            {
                "statusCode": 400,
                "message": "Parameter invalid! artist must have minimal 2 characters"
            }
        """
        try:
            validate_get_concerts_event(parameters)
        except AssertionError as error:
            raise BadRequestError(f'Parameter invalid! {str(error)}')

        return self.repository.find_concerts_by_artist(parameters.get('artist'))
        
        
    def put_concert_action(self, parameters: dict, body: dict) -> Concert:
        """
        Example:
            controller.put_concert_action({
                "artist": "Madonna",
                "concert": "This is Madonna 2023",
                "ticket_sales": 5000000
            })

        :return: The created concert. Example:
            {
                "artist": "Madonna",
                "concert": "This is Madonna 2023",
                "ticket_sales": 5000000,
                "created_date": "2023-09-08T14:47:29.915661"
            }

        :raises BadRequestError: For validation errors. Example:
            {
                "statusCode": 400,
                "message": "Parameter invalid! artist must have minimal 2 characters"
            }
        """
        try:
            validate_put_concert_event(body)
        except AssertionError as error:
            raise BadRequestError(f'Parameter invalid! {str(error)}')

        return self.repository.create_concert(body)
