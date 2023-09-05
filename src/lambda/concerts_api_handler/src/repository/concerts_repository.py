from __future__ import annotations
from typing import TypedDict
import os

import boto3
from boto3.dynamodb.conditions import Key, Attr

from model.concert import Concert
from repository.dynamodb_helpers import to_dynamodb_record


class ConcertsRepository:
    def __init__(self, dynamodb_resource=boto3.resource('dynamodb')) -> ConcertsRepository:
        """
        Example:
            os.environ['TABLE_NAME'] = 'concerts'
            
            from repository.concerts_repository import ConcertsRepository

            repository = ConcertsRepository()

        :return: A ConcertsRepository instance
        """
        self.table_name = os.environ.get('TABLE_NAME')
        self.table = dynamodb_resource.Table(self.table_name)

    def find_concerts_by_artist(self, artist: str) -> list[dict]:
        """
        Finds all concerts that match the given artist

        Example:
            repository = ConcertsRepository()
            repository.find_concerts_by_artist('Madonna')

        :return: A list of concerts
        """
        query_response = self.table.query(
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('artist').eq(artist)
        )
        return query_response['Items']
        
        
    def create_concert(self, concert: Concert) -> Concert:
        """
        Add a new concert to the DB

        Example:
            repository = ConcertsRepository()
            repository.add_concert({
                'artist': 'Zoe',
                'concert': 'French tales',
                'ticket_sales': 80000
            })

        :return: The added concert
        """
        put_response = self.table.put_item(
            Item=to_dynamodb_record(concert),
            ReturnValues='ALL_NEW'
        )
        return put_response['Attributes']
