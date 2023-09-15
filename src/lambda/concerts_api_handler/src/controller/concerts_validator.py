def validate_get_concerts_event(event: dict) -> None:
    """
    Validates a GET concerts Lambda event

    Example:
        self.validate_get_concerts_event(
            { "artist": "Madonna" }
        )

    :param dict event:          Must be DEFINED
    :param str event.artist:    Must have LENGTH > 2

    :raises AssertionError: In case of invalid properties
    """
    assert bool(event), 'event empty'

    expected_parameters = set(['artist'])
    unexpected_parameters = set(event.keys()) - expected_parameters
    assert not bool(unexpected_parameters), f'Unexpected event parameters: {",".join(unexpected_parameters)}. Expected only: {",".join(expected_parameters)}'

    artist = event.get('artist')

    assert bool(artist) and len(artist) > 2, 'artist must have minimal 2 characters'


def validate_put_concert_event(event: dict) -> None:
    """
    Validates a PUT concert Lambda event

    Example:
        self.validate_get_concerts_event({
            "artist": "Madonna",
            "concert": "This is Madonna 2023",
            "ticket_sales": 5000000
        })

    :param dict event:              Must be DEFINED
    :param str event.artist:        Must have LENGTH > 2
    :param str event.concert:       Must have LENGTH > 2
    :param int event.ticket_sales:  Must be > 0

    :raises AssertionError: In case of invalid properties
    """
    assert bool(event), 'event empty'

    expected_parameters = set(['artist', 'concert', 'ticket_sales'])
    unexpected_parameters = set(event.keys()) - expected_parameters
    assert not bool(unexpected_parameters), f'Unexpected event parameters: {",".join(unexpected_parameters)}. Expected only: {",".join(expected_parameters)}'

    artist = event.get('artist')
    assert bool(artist) and len(artist) > 2, 'artist must have minimal 2 characters'
    
    concert = event.get('concert')
    assert bool(concert) and len(concert) > 2, 'concert must have minimal 2 characters'
    
    ticket_sales = event.get('ticket_sales')
    assert bool(ticket_sales) and ticket_sales >0, 'ticket_sales must be greater than 0'
