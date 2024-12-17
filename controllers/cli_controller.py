from flask import Blueprint

from init import db
from models.address import Address
from models.faculty import Faculty
from models.student import Student
from models.professor import Professor
from models.degree_level import Degree_level
from models.thesis import Thesis

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
            street_number="14",
            street="Bacon Road",
            suburb="Richmond",
            postcode="3121",
            state="Vic",
        ),
        Address(
            street_number="7",
            street="Crackle Street",
            suburb="Bundoora",
            postcode="3083",
            state="Vic",
        ),
        Address(
            street_number="31",
            street="Chicken Road",
            suburb="Gippsland",
            postcode="3841",
            state="Vic",
        ),
        Address(
            street_number="24",
            street="Lolly Court",
            suburb="Shepparton",
            postcode="3630",
            state="Vic",
        ),
        Address(
            street_number="9",
            street="Clinker Street",
            suburb="Boronia",
            postcode="3155",
            state="Vic",
        ),
    ]
    db.session.add_all(addresses)
    db.session.commit()

    faculties = [
        Faculty(faculty_name="Department of Environment and Genetics"),
        Faculty(faculty_name="Department of Nursing and Midwifery"),
        Faculty(faculty_name="Department of Law"),
        Faculty(faculty_name="Department of Humanities and Social Sciences"),
        Faculty(
            faculty_name="Department of Computing, Engineering, and Mathematical Sciences"
        ),
    ]
    db.session.add_all(faculties)
    db.session.commit()

    students = [
        Student(
            name = "Jane Doe",
            phone = "0100000000",
            email = "janedoe@email.com",
            address_id = addresses[0].id
        ),
         Student(
            name = "Bob Cob",
            phone = "0100000001",
            email = "bobcob@op.com",
            address_id = addresses[1].id
        ),
         Student(
            name = "John Doe",
            phone = "0100000002",
            email = "johndoe@email.com",
            address_id = addresses[0].id
        ),
         Student(
            name = "Cain Smith",
            phone = "0100000003",
            email = "cainsmith@box.com",
            address_id = addresses[2].id
        ),
         Student(
            name = "Maisy Mouse",
            phone = "0100000004",
            email = "maisymouse@maze.com",
            address_id = addresses[3].id
        ),
          Student(
            name = "Stacy Lark",
            phone = "0100000005",
            email = "stacylark@pol.com",
            address_id = addresses[4].id
        )
    ]
    db.session.add_all(students)
    db.session.commit()
    
    professors = [
        Professor(
            name = "Gareth Plain",
            phone = "0300000000",
            email = "garethplain@university.com",
            faculty_id = faculties[0].id
        ),
         Professor(
            name = "Hayley Blue",
            phone = "0300000001",
            email = "hayleyblue@university.com",
            faculty_id = faculties[1].id
        ),
         Professor(
            name = "Sonia Marie",
            phone = "0300000002",
            email = "soniamarie@university.com",
            faculty_id = faculties[1].id
        ),
         Professor(
            name = "Luke Sky",
            phone = "0300000003",
            email = "lukesky@university.com",
            faculty_id = faculties[2].id
        ),
         Professor(
            name = "Sebastien Park",
            phone = "0300000004",
            email = "sebastienpark@university.com",
            faculty_id = faculties [3].id
        ),
         Professor(
            name = "Bonnie Tree",
            phone = "0300000005",
            email = "bonnietree@university.com",
            faculty_id = faculties [4].id
         )
    ]
    db.session.add_all(professors)
    db.session.commit()

    degree_levels=[
        Degree_level(
            degree_level_name = "Honours"
        ),
        Degree_level(
            degree_level_name = "Masters"
        ),
        Degree_level(
            degree_level_name = "PHD"
        )
    ]

    db.session.add_all(degree_levels)
    db.session.commit()

    theses=[
        Thesis(
            name = "Determining the age of Dingos from faecal samples",
            grade = "A",
            student_id = students[0].id,
            degree_level_id = degree_levels[0].id
        ),
         Thesis(
            name = "Modern influence on the practice of law",
            grade = "B",
            student_id = students[1].id,
            degree_level_id = degree_levels[1].id
        ),
         Thesis(
            name = "Arts impact on modern society",
            grade = "B",
            student_id = students[2].id,
            degree_level_id = degree_levels[2].id
        ),
         Thesis(
            name = "The Valuable Lessons of Poker",
            grade = "D",
            student_id = students[3].id,
            degree_level_id = degree_levels[1].id
        ),    
         Thesis(
            name = "Gene Therapy for Cancer Treatment",
            grade = "C",
            student_id = students[4].id,
            degree_level_id = degree_levels[0].id
        )
    ]   
    db.session.add_all(theses)
    db.session.commit()
    print("tables seeded")
