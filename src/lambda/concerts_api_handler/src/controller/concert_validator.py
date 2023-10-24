def validate_get_concerts_event(event: dict) -> None:
    """
    Validates a GET concerts Lambda event

    Example:
        self.validate_get_concerts_event(
            { "artist": "Madonna" }
        )

    :param event:           Validation: Must be DEFINED
    :type event: dict

    :param event.artist:    Validation: Must be DEFINED
    :type: event.artist: str

    :raises AssertionError: In case of invalid properties
    """
    assert bool(event), 'event empty'

    expected_parameters = ['artist']
    unexpected_parameters = set(expected_parameters).symmetric_difference(
        set(event.keys())
    )
    assert len(unexpected_parameters) == 0, \
        f'Unexpected event parameters: {",".join(unexpected_parameters)}. Expected only: {",".join(expected_parameters)}'


def validate_put_concert_event(event: dict) -> None:
    """
    Validates a PUT concert Lambda event

    Example:
        self.validate_get_concerts_event({
            "artist": "Madonna",
            "concert": "This is Madonna 2023",
            "ticket_sales": 5000000
        })

    :param event:               Validation: Must be DEFINED
    :type event: dict

    :param dto.artist:          Validation: Must be DEFINED
    :type dto.artist: str

    :param dto.concert:         Validation: Must be DEFINED
    :type dto.concert: str

    :param dto.ticket_sales:    Validation: Must be DEFINED
    :type dto.ticket_sales: int

    :raises AssertionError: In case of invalid properties
    """
    assert bool(event), 'event empty'

    expected_parameters = ['artist', 'concert', 'ticket_sales']
    unexpected_parameters = set(expected_parameters).symmetric_difference(
        set(event.keys())
    )
    assert len(unexpected_parameters) == 0, \
        f'Unexpected or missing event parameters: {",".join(unexpected_parameters)}. Expected only: {",".join(expected_parameters)}'
