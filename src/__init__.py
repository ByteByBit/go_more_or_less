import logging

from src.db import RidesTable
from src.parameters import Parameters
from src.utils import CMDs, Texts, print_out, convert_db_rows_to_str


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def retrieve_rides(params: Parameters) -> list:
    ''' Retrieve rides stored  in DB.'''

    logging.info('Retrieving ride(s).')

    result = RidesTable.get_rides(args=params)
    
    return convert_db_rows_to_str(rows=result)


def register_ride(params: Parameters) -> None:
    ''' Register ride in DB.'''

    logging.info('Create ride.')

    res = RidesTable(
        from_city=params.from_city, 
        to_city=params.to_city, 
        date=params.from_date, 
        num_seats=params.num_seats
    )
    res.commit()


def register_return_trip(params: Parameters) -> bool:
    ''' Register return-ride in DB.'''

    logging.info('Create return-trip.')

    last_ride = RidesTable.get_last_inserted()

    params.from_city = last_ride.to_city
    params.to_city = last_ride.from_city
    params.num_seats = last_ride.num_seats

    register_ride(params=params)


def handle_request(req: str):
    ''' Handles user requests.'''

    cmd_list = req.split(' ')

    cmd = cmd_list[0] # Get the cmd indicator, [S, C, R].

    cmd_list.pop(0) # Remove cmd indicator.

    args = cmd_list[:] # Make a new list, to reset indexing.

    params = Parameters(args=args)
    params.parse()

    # Create ride.
    if cmd in CMDs.create_ride:
        
        try:
            register_ride(params=params)

        except Exception as e:
            logging.error(
                f'Registering trip failed: {e}'
            )

    # Retrieve ride(s).
    elif cmd in CMDs.retrieve_ride:

        try:
            res = retrieve_rides(params=params)
            print_out(txt=res)
            
        except Exception as e:
            logging.error(
                f'Retreiving data failed: {e}'
            )

    # Create return ride.
    elif cmd in CMDs.create_return_ride:

        try:
            register_return_trip(params=params)

        except Exception as e:
            logging.error(
                f'Registering return trip failed: {e}'
            )


def wait_input():
    ''' Waiting user input in an infinite loop.'''

    val = input('>')
    
    # User quits.
    if val in CMDs.quit:
        print_out(Texts.farewell)
        quit()

    # User wants help, so display it.
    elif val in CMDs.help:
        print_out(Texts.help_txt)

    # Actual commands start here.
    else:

        handle_request(req=val)
   
    
    wait_input() # Start over, might be other requests.


def main():

    print(Texts.welcome)
    wait_input()