from unittest import TestCase
from os import linesep
import logging

from src import retrieve_rides, register_ride, register_return_trip
from src.parameters import Parameters


class TestScript(TestCase):

    
    def test_retrieve_rides(self):
        ''' '''

        args = [
            [Parameters(args=[]), f'Odense Copenhagen 2018-10-01 4 {linesep}'], # S
            [Parameters(args=['2018-10-01']), f'Odense Copenhagen 2018-10-01 4 {linesep}'], # S 2018-10-01
            [Parameters(args=['2018-10-01', '4']), f'Odense Copenhagen 2018-10-01 4 {linesep}'], # S 2018-10-01 4
            [Parameters(args=['2018-10-01', '7']), ''], # S 2018-10-01 7
            [Parameters(args=['2018-10-01', '2', 'Odense']), f'Odense Copenhagen 2018-10-01 4 {linesep}'], # S Odense 2018-10-01 2
            [Parameters(args=['2018-10-01', 'Aarhus']), ''], # S 2018-10-01 Aarhus
            [Parameters(args=['2020-10-01', 'Aarhus']), ''], # S 2020-10-01 Aarhus
            [Parameters(args=['2020-10-01', 'Odense']), ''] # S 2020-10-01 Odense
        ]

        for arg in args:
            
            arg[0].parse()
            self.assertEqual(retrieve_rides(arg[0]), arg[1])

        logging.info('Test passed for: retrieve_rides')

    def test_register_ride(self):
        ''' '''

        params = Parameters(args=['Odense', 'Copenhagen', '2018-10-01', '4'])
        params.parse()
        self.assertEqual(register_ride(params=params), None)

        logging.info('Test passed for: register_ride')

    def test_register_return_trip(self):
        ''' '''

        params = Parameters(args=['2018-10-01'])
        params.parse()
        self.assertEqual(register_return_trip(params=params), None)

        logging.info('Test passed for: register_return_trip')


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

test = TestScript()
test.test_register_ride()
test.test_retrieve_rides()
test.test_register_return_trip()
