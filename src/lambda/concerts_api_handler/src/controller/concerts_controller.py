from __future__ import annotations
import os
import re

from aws_lambda_powertools.event_handler.exceptions import BadRequestError

from model.concer import Concert
from repository.concerts_repository import ConcertsRepository
from concerts_validator import validate_get_concerts_event, validate_put_concert_event


class ConcertsController:
    def __init__(self, repository: ConcertsRepository) -> ConcertsController:
        """
        Example:
            from repository.concerts_repository import ConcertsRepository
            from controller.concerts_controller import ConcertsController
            
            repository = ConcertsRepository()
            controller = ConcertsController(repository)

        Returns:
            A ConcertsController instance
        """
        self.repository = repository

    def get_concerts_action(self, event: dict) -> list[Concert]:
        """
        Example:
            controller.get_concerts_action(
                { "artist": "Madonna" }
            )

        Returns:
            A list of concerts matching the event parameters. Example:
                [
                    {
                        "artist": "Madonna",
                        "concert": "This is Madonna 2023",
                        "ticket_sales": 5000000
                    },
                    ...
                ]

        Raises:
            400 BadRequestError validation error. Example:
                {
                    "statusCode": 400,
                    "message": "Parameter invalid! artist must have minimal 2 characters"
                }
        """
        try:
            validate_get_concerts_event(event)
        except AssertionError as error:
            raise BadRequestError(f'Parameter invalid! {str(error)}')

        return self.repository.find_concerts_by_artist(event.get('artist'))
        
        
    def put_concert_action(self, event: dict) -> Concert:
        """
        Example:
            controller.get_concerts_action({
                "artist": "Madonna",
                "concert": "This is Madonna 2023",
                "ticket_sales": 5000000
            })

        Returns:
            The created concert. Example:
                {
                    "artist": "Madonna",
                    "concert": "This is Madonna 2023",
                    "ticket_sales": 5000000
                }

        Raises:
            400 BadRequestError validation error. Example:
                {
                    "statusCode": 400,
                    "message": "Parameter invalid! artist must have minimal 2 characters"
                }
        """
        try:
            validate_put_concert_event(event)
        except AssertionError as error:
            raise BadRequestError(f'Parameter invalid! {str(error)}')

        return self.repository.create_concert(event)
