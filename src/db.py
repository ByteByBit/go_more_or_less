from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false
from sqlalchemy.orm import sessionmaker


db_engine = create_engine('sqlite:///db/rides.db')
Base = declarative_base(bind=db_engine)
Session = sessionmaker(bind=db_engine)


class RidesTable(Base):
    ''' DB model class.'''

    __tablename__ = 'rides'

    id = Column(Integer(), primary_key=True)
    from_city = Column(String(255), nullable=false)
    to_city = Column(String(255), nullable=false)
    date = Column(Date, nullable=false)
    num_seats = Column(Integer())
    created = Column(DateTime, nullable=false, onupdate=datetime.now)

    def __init__(
        self, from_city: str, to_city: str, date: datetime, num_seats: int) -> None:
        
        self.from_city = from_city
        self.to_city = to_city
        self.date = date
        self.num_seats = int(num_seats)

    @staticmethod
    def param_builder(args: list) -> list:
        ''' Builds params for DB query.'''

        params = []

        # Both from and to date are set.
        if args.from_date and args.to_date:
            params.append(RidesTable.date >= args.from_date)
            params.append(RidesTable.date <= args.to_date)

        # Only 1 date is supplied.
        elif args.from_date :
            params.append(RidesTable.date == args.from_date)
        
        # Starting city supplied.
        if args.from_city:
            params.append(RidesTable.from_city == args.from_city)

        # Destination city supplied.
        if args.to_city:
            params.append(RidesTable.to_city == args.to_city)

        # Min nr of seats supplied.
        if args.num_seats:
            params.append(RidesTable.num_seats >= args.num_seats)

        return params

    @staticmethod
    def get_rides(args) -> list:
        ''' Returns registered rides based on supplied params.'''

        params = RidesTable.param_builder(args=args)
        
        with Session() as session:
            return session.query().with_entities(
                RidesTable.from_city,
                RidesTable.to_city,
                RidesTable.date,
                RidesTable.num_seats
                ).filter(*params).all()

    @staticmethod
    def get_last_inserted() -> list:
        ''' Returns last registered ride.'''

        with Session() as session:
            return session.query().with_entities(
                RidesTable.from_city,
                RidesTable.to_city,
                RidesTable.date,
                RidesTable.num_seats
                ).order_by(RidesTable.id.desc()).first()

    def commit(self) -> bool:
        ''' Insert into DB.'''

        with Session() as session:

            session.add(self)
            try:
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return False


Base.metadata.create_all(db_engine)
