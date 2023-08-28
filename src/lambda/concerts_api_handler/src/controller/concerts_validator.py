def validate_get_concerts_event(event: dict) -> None:
    """
    Validates a GET concerts Lambda event

    Parameters:
        - event p           DEFINED
        - p.artist          LENGTH > 2

    Example:
        self.validate_get_concerts_event(
            { "artist": "Madonna" }
        )

    Raises:
        An AssertionError in case of invalid properties
    """
    assert bool(event), 'event empty'

    assert not bool(
        set(event.keys()) - set(('artist'))
    ), 'Unexpected event. Expected only concerts parameter.'

    artist = event.get('artist')

    assert bool(artist) and len(artist) > 2, 'artist must have minimal 2 characters'


def validate_put_concert_event(event: dict) -> None:
    """
    Validates a PUT concert Lambda event

    Parameters:
        - event p           DEFINED
        - p.artist          LENGTH > 2
        - p.concert         LENGTH > 2
        - p.ticket_sales    > 0

    Example:
        self.validate_get_concerts_event({
            "artist": "Madonna",
            "concert": "This is Madonna 2023",
            "ticket_sales": 5000000
        })

    Raises:
        An AssertionError in case of invalid properties
    """
    assert bool(event), 'event empty'

    assert not bool(
        set(event.keys()) - set(('artist', 'concert', 'sales'))
    ), 'Unexpected event. Expected only concerts parameter.'

    artist = event.get('artist')
    assert bool(artist) and len(artist) > 2, 'artist must have minimal 2 characters'
    
    concert = event.get('concert')
    assert bool(concert) and len(concert) > 2, 'concert must have minimal 2 characters'
    
    ticket_sales = event.get('ticket_sales')
    assert bool(ticket_sales) and ticket_sales >0, 'ticket_sales must be greater than 0'
