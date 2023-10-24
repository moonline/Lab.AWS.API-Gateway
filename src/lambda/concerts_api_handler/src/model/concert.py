from __future__ import annotations

from datetime import datetime


class Concert:
    @staticmethod
    def validate(dto: dict) -> None:
        """
        Validate a concert data transfer object

        Example:
            dto = {
                "artist": "Madonna",
                "concert": "This is Madonna 2023",
                "ticket_sales": 5000000,
                "create_date": "2023-09-08T14:47:29.915661"
            }
            Concert.validate(dto)

        :param dto:                 Validation: Must be DEFINED
        :type dto: dict

        :param dto.artist:          Validation: Must have more than 2 characters
        :type dto.artist: str

        :param dto.concert:         Validation: Must have more than 2 characters
        :type dto.concert: str

        :param dto.ticket_sales:    Validation: Must be a positive number
        :type dto.ticket_sales: int

        :raises AssertionError: In case of invalid properties
        """
        assert bool(dto), 'concert DTO should not be empty'

        artist = dto.get('artist')
        assert bool(artist) and len(artist) > 2, \
            'artist must have minimal 2 characters'

        concert = dto.get('concert')
        assert bool(concert) and len(concert) > 2, \
            'concert must have minimal 2 characters'

        ticket_sales = dto.get('ticket_sales')
        assert bool(ticket_sales) and ticket_sales >= 0, \
            'ticket_sales must be a positive amount'

    @classmethod
    def from_dto(cls, dto: dict) -> Concert:
        """
        Create a concert from a data transfer object (dict)

        Example:
            dto = {
                "artist": "Madonna",
                "concert": "This is Madonna 2023",
                "ticket_sales": 5000000,
                "create_date": "2023-09-08T14:47:29.915661"
            }
            concert = Concert.from_dto(dto)

        :param dto: A concert DTO (dict)
        :type dto: dict

        :raises AssertionError: In case of invalid properties

        :return: A new Concert
        :rtype: Concert
        """
        cls.validate(dto)

        return cls(
            dto['artist'],
            dto['concert'],
            dto['ticket_sales'],
            (
                datetime.fromisoformat(dto['create_date'])
                if dto.get('create_date') else None
            )
        )

    def __init__(self, artist: str, concert: str, ticket_sales: int, create_date: datetime) -> Concert:
        """
        Example:
            concert = Concert(
                "Madonna",
                "This is Madonna 2023",
                5000000,
                datetime(2023,09,08,14,47,29,915661)
            )

        :param artist: Concert artist
        :type artist: str

        :param concert: Concert name
        :type concert: str

        :param ticket_sales: Total ticket sales
        :type ticket_sales: int

        :param create_date: Concert creation date
        :type create_date: datetime, optional

        :return: A Concert instance
        :rtype: Concert
        """
        self.artist = artist
        self.concert = concert
        self.ticket_sales = ticket_sales
        self.create_date = create_date

    @property
    def dto(self) -> dict:
        """
        :return: The Concert as data transfer object (dict). Example:
            {
                "artist": "Madonna",
                "concert": "This is Madonna 2023",
                "ticket_sales": 5000000,
                "create_date": "2023-09-08T14:47:29.915661"
            }
        :rtype: dict
        """
        return {
            'artist': self.artist,
            'concert': self.concert,
            'ticket_sales': self.ticket_sales,
            'create_date': self.create_date.isoformat()
        }
