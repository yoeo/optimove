# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from . import URLBuilder


class Model(URLBuilder):
    client = None

    def __init__(self, client):
        self.client = client

    def get_customer_attribute_list(self):
        """Returns all the available customer attribute names (which can be passed to certain other functions
        as an input parameter) and a description of each."""
        response = self.client.get(self._get_url())
        if not response:
            return False

        results = {}
        for item in response.json():
            results[item['RealFieldName']] = item['Description']

        return results

    def get_lifecycle_stage_list(self):
        """Returns all available lifecycle stages (for use in other functions, e.g., GetCustomerFutureValues)."""
        response = self.client.get(self._get_url())
        if not response:
            return False

        results = {}
        for item in response.json():
            results[item['StageId']] = item['StageName']

        return results

    def get_microsegment_list(self):
        """Returns an dict containing the details of all microsegments."""
        response = self.client.get(self._get_url())
        if not response:
            return False

        results = {}
        for item in response.json():
            results[item['MicrosegmentID']] = item['MicrosegmentName']

        return results

    def get_microsegment_changers(self, start, end, attributes=None, delimiter=';'):
        """Returns an array of customer IDs, and their before and after micro-segment IDs,
        for customers whose micro-segment changed during a particular date range."""
        data = {
            'StartDate': start,
            'EndDate': end
        }
        if attributes and type(attributes) == type(list):
            attributes = ';'.join(attributes)
            data['CustomerAttributes'] = attributes

            if delimiter:
                if delimiter in (';', ',', ':', '/', '?', '&', '#', '%', '$', '+', '='):
                    data['CustomerAttributesDelimiter'] = delimiter
                else:
                    raise Exception('Invalid delimiter')

        response = self.client.get(self._get_url())
        if not response:
            return False

        results = list()
        for item in response.json():
            result = {
                'customer_id': item['CustomerID'],
                'initial': item['InitialMicrosegment'],
                'final': item['FinalMicrosegment']
            }
            if attributes:
                customer_attributes = item['CustomerAttributes'].split(delimiter)
                for index, attribute in enumerate(attributes):
                    result['attributes'][attribute] = customer_attributes[index]
            results.append(result)

        return results
