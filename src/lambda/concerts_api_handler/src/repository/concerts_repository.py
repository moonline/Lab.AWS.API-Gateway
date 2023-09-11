from __future__ import annotations
from typing import TypedDict
import os
from datetime import datetime
from functools import reduce

import boto3
from boto3.dynamodb.conditions import Key, Attr

from model.concert import Concert


dynamodb_resource = boto3.resource('dynamodb')


class ConcertsRepository:
    def __init__(self, dynamodb_resource=dynamodb_resource) -> ConcertsRepository:
        """
        Example:
            os.environ['TABLE_NAME'] = 'concerts'
            
            from repository.concerts_repository import ConcertsRepository

            repository = ConcertsRepository()

        :return: A ConcertsRepository instance
        """
        self.table_name = os.environ.get('TABLE_NAME')
        self.dynamodb_table = dynamodb_resource.Table(self.table_name)

    def find_concerts_by_artist(self, artist: str) -> list[dict]:
        """
        Finds all concerts that match the given artist

        Example:
            repository = ConcertsRepository()
            repository.find_concerts_by_artist('Madonna')

        :return: A list of concerts
        """
        paginator = self.dynamodb_table.meta.client.get_paginator('query')
        page_iterator = paginator.paginate(
            TableName=self.table_name,
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('artist').eq(artist)
        )
        return reduce(
            lambda a, b: a+b,
            [page['Items'] for page in page_iterator]
        )


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
        record = {
            **concert,
            'created_date': datetime.now().isoformat()
        }
        put_response = self.dynamodb_table.put_item(
            Item=record,
            ReturnValues='ALL_OLD'
        )
        if put_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return record
        else:
            raise Exception("An error occured when storing the concert")
