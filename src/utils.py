from os import linesep


class CMDs:
    ''' Acceptable commands.'''

    quit = ['q', 'quit', 'escape', 'exit', 'leave me alone']
    help = ['h', 'help', 'the hell is this']
    create_ride = ['c', 'C']
    retrieve_ride = ['s', 'S']
    create_return_ride = ['r', 'R']


class Texts:
    ''' UI texts.'''

    help_txt = '''Available commands:
Quit: 'q', 'quit', 'escape', 'exit', 'leave me alone',
Help: 'h', 'help', 'the hell is this',
Create a new ride: 'c' or 'C' followed by an origin city name, a destination city name, 
a date and finally the number of available seats.
Example: C Odense Copenhagen 2018-10-01 4
Create a return trip: 'r' or 'R' followed by a date.
Example: R 2018-10-01
Retrieve registered rides: 'S' optionally followed by origin city, destination city, from and/or to date, min. available seats.
Example: S Odense Copenhagen 2018-10-01 2018-10-03 2
Note: 
- Each and every argument is separated by a space char
- The dates are Unix dates, separated by a hyphen, YYYY-MM-DD
'''
    welcome = f'What can I do for you today? {linesep}Type help for the available commands!{linesep}'
    farewell = 'Have a good one, mate!'


def print_out(txt: str) -> None:

    final_txt = f'=>{linesep}{txt}'
    print(final_txt)


def convert_db_rows_to_str(rows):
    ''' Converts retrieved DB rows to human friendly str.'''

    txt = ''
    for row in rows:
        txt += f'{row.from_city} {row.to_city} {row.date} {row.num_seats} {linesep}'
    
    return txt
