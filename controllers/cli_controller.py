from flask import Blueprint

from init import db
from models.address import Address

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command("seed")
def seed_tables():
    addresses = [
        Address(
            street_number = "14",
            street = "Bacon Road",
            suburb = "Richmond",
            postcode = "3121"   , 
            state = "Vic" 
        ),
        
        Address(
                street_number = "7",
                street = "Crackle Street",
                suburb = "Bundoora",
                postcode = "3083",    
                state = "Vic" 
            ),
        
        Address(
            street_number = "31",
            street = "Chicken Road",
            suburb = "Gippsland",
            postcode = "3841",    
            state = "Vic"
        ),

        Address(
            street_number = "24",
            street = "Lolly Court",
            suburb = "Shepparton",
            postcode = "3630",    
            state = "Vic" 
        ),
        Address(
                street_number = "9",
                street = "Clinker Street",
                suburb = "Boronia",
                postcode = "3155",    
                state = "Vic" 
            )


    ]
    db.session.add_all(addresses)
    db.session.commit()
    print("tables seeded")