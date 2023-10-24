from __future__ import annotations

from model.concert import Concert
from repository.concert_repository import ConcertRepository
from controller.concert_validator import validate_get_concerts_event, validate_put_concert_event


class ConcertController:
    def __init__(self, repository: ConcertRepository) -> ConcertController:
        """
        Example:
            from repository.concert_repository import ConcertRepository
            from controller.concert_controller import ConcertController

            repository = ConcertRepository()
            controller = ConcertController(repository)

        :param repository: A repository to interact with persistence
        :type repository: ConcertRepository

        :return: A ConcertController instance
        :rtype: ConcertController
        """
        self.repository = repository

    def get_concerts_action(self, parameters: dict, body: dict) -> list[Concert]:
        """
        Example:
            controller.get_concerts_action(
                { "artist": "Madonna" },
                {}
            )

        :param parameters: API GW url parameters. Example:
            { "artist": "Madonna" }
        :type parameters: dict

        :param body: API GW request body. Example:
            {}
        :type body: dict

        :raises BadRequestError: For validation errors. Example:
            {
                "statusCode": 400,
                "message": "Parameter invalid! artist must have minimal 2 characters"
            }

        :return: A list of concerts matching the parameters. Example:
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
        try:
            validate_get_concerts_event(parameters)
        except AssertionError as error:
            return (
                {
                    'message': f'Parameter invalid! {str(error)}'
                },
                400
            )

        return [
            concert.dto
            for concert in self.repository.find_concerts_by_artist(parameters.get('artist'))
        ]

    def put_concert_action(self, parameters: dict, body: dict) -> Concert:
        """
        Example:
            controller.put_concert_action(
                {},
                {
                    "artist": "Madonna",
                    "concert": "This is Madonna 2023",
                    "ticket_sales": 5000000
                }
            )

        :param parameters: API GW url parameters. Example:
            {}
        :type parameters: dict

        :param body: API GW request body. Example:
            {
                "artist": "Madonna",
                "concert": "This is Madonna 2023",
                "ticket_sales": 5000000
            }
        :type body: dict

        :raises BadRequestError: For validation errors. Example:
            {
                "statusCode": 400,
                "message": "Parameter invalid! artist must have minimal 2 characters"
            }

        :return: The created concert. Example:
            {
                "artist": "Madonna",
                "concert": "This is Madonna 2023",
                "ticket_sales": 5000000,
                "create_date": "2023-09-08T14:47:29.915661"
            }
        :rtype: dict
        """
        try:
            validate_put_concert_event(body)
            concert = Concert.from_dto(body)
        except AssertionError as error:
            return (
                {
                    'message': f'Parameter invalid! {str(error)}'
                },
                400
            )

        return self.repository.create_concert(concert).dto
