from __future__ import annotations

import os
from datetime import datetime
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

from model.concert import Concert


dynamodb_resource = boto3.resource('dynamodb')


class ConcertRepository:
    @staticmethod
    def concert_to_record(concert: Concert) -> dict:
        return {
            'artist': concert.artist,
            'concert': concert.concert,
            'ticket_sales': Decimal(concert.ticket_sales),
            'create_date': Decimal(concert.create_date.timestamp())
        }

    @staticmethod
    def record_to_concert(record: dict) -> Concert:
        return Concert(
            record['artist'],
            record['concert'],
            float(record['ticket_sales']),
            datetime.fromtimestamp(record['create_date'])
        )

    def __init__(self, dynamodb_resource=dynamodb_resource) -> ConcertsRepository:
        """
        Example:
            os.environ['TABLE_NAME'] = 'concerts'

            from repository.concert_repository import ConcertRepository

            repository = ConcertRepository()

        :param dynamodb_resource: A boto3 DynamoDB resource
        :type dynamodb_resource: boto3.resource

        :return: A ConcertRepository instance
        :rtype: ConcertRepository
        """
        self.table_name = os.environ.get('TABLE_NAME')
        self.table = dynamodb_resource.Table(self.table_name)

    def find_concerts_by_artist(self, artist: str) -> list[Concert]:
        """
        Finds all concerts that match the given artist

        Example:
            repository = ConcertRepository()
            repository.find_concerts_by_artist('Madonna')

        :param artist: An artist name
        :type artist: str

        :return: A list of concerts
        :rtype: list
        """
        paginator = self.table.meta.client.get_paginator('query')
        page_iterator = paginator.paginate(
            TableName=self.table_name,
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('artist').eq(artist)
        )

        return [
            self.record_to_concert(concert_record)
            for page in page_iterator
            for concert_record in page['Items']
        ]

    def create_concert(self, concert: Concert) -> Concert:
        """
        Add a new concert to the database

        Example:
            repository = ConcertRepository()
            concert = Concert(
                'Zoe',
                'French tales',
                80000
            )
            repository.add_concert(concert)

        :param concert: A concert object to be persisted
        :type concert: Concert

        :return: The persisted concert
        :rtype: Concert
        """
        concert.create_date = datetime.now()
        record = self.concert_to_record(concert)

        put_response = self.table.put_item(
            Item=record,
            ReturnValues='ALL_OLD'
        )
        if put_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return concert
        else:
            raise Exception("An error occurred when storing the concert")
