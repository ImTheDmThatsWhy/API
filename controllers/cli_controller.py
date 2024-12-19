from flask import Blueprint

from init import db
from models.address import Address
from models.faculty import Faculty
from models.student import Student
from models.supervisor import Supervisor
from models.status import Status
from models.thesis import Thesis
from models.student_supervisors import Student_supervisor

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
            name="Jane Doe",
            phone="0100000000",
            email="janedoe@email.com",
            address_id=addresses[0].id,
        ),
        Student(
            name="Bob Cob",
            phone="0100000001",
            email="bobcob@op.com",
            address_id=addresses[1].id,
        ),
        Student(
            name="John Doe",
            phone="0100000002",
            email="johndoe@email.com",
            address_id=addresses[0].id,
        ),
        Student(
            name="Cain Smith",
            phone="0100000003",
            email="cainsmith@box.com",
            address_id=addresses[2].id,
        ),
        Student(
            name="Maisy Mouse",
            phone="0100000004",
            email="maisymouse@maze.com",
            address_id=addresses[3].id,
        ),
        Student(
            name="Stacy Lark",
            phone="0100000005",
            email="stacylark@pol.com",
            address_id=addresses[4].id,
        ),
    ]
    db.session.add_all(students)
    db.session.commit()

    supervisors = [
        Supervisor(
            name="Gareth Plain",
            phone="0300000000",
            email="garethplain@university.com",
            faculty_id=faculties[0].id,
        ),
        Supervisor(
            name="Hayley Blue",
            phone="0300000001",
            email="hayleyblue@university.com",
            faculty_id=faculties[1].id,
        ),
        Supervisor(
            name="Sonia Marie",
            phone="0300000002",
            email="soniamarie@university.com",
            faculty_id=faculties[1].id,
        ),
        Supervisor(
            name="Luke Sky",
            phone="0300000003",
            email="lukesky@university.com",
            faculty_id=faculties[2].id,
        ),
        Supervisor(
            name="Sebastien Park",
            phone="0300000004",
            email="sebastienpark@university.com",
            faculty_id=faculties[3].id,
        ),
        Supervisor(
            name="Bonnie Tree",
            phone="0300000005",
            email="bonnietree@university.com",
            faculty_id=faculties[4].id,
        ),
    ]
    db.session.add_all(supervisors)
    db.session.commit()

    statuses = [
        Status(status_name="Passed"),
        Status(status_name="Failed"),
        Status(status_name="Passed with revisions"),
        Status(status_name="Needs revision"),
        Status(status_name="Being reviewed"),
    ]

    db.session.add_all(statuses)
    db.session.commit()

    theses = [
        Thesis(
            name="Determining the age of Dingos from faecal samples",
            student_id=students[0].id,
            status_id=statuses[0].id,
        ),
        Thesis(
            name="Modern influence on the practice of law",
            student_id=students[1].id,
            status_id=statuses[1].id,
        ),
        Thesis(
            name="Arts impact on modern society",
            student_id=students[2].id,
            status_id=statuses[2].id,
        ),
        Thesis(
            name="The Valuable Lessons of Poker",
            student_id=students[3].id,
            status_id=statuses[3].id,
        ),
        Thesis(
            name="Gene Therapy for Cancer Treatment",
            student_id=students[4].id,
            status_id=statuses[4].id,
        ),
        Thesis(
            name="The effects of natural oxytocin in labour",
            student_id=students[5].id,
            status_id=statuses[4].id,
        ),
    ]
    db.session.add_all(theses)
    db.session.commit()

    student_supervisor = [
        Student_supervisor(student_id=students[0].id, supervisor_id=supervisors[0].id),
        Student_supervisor(student_id=students[1].id, supervisor_id=supervisors[1].id),
        Student_supervisor(student_id=students[1].id, supervisor_id=supervisors[2].id),
        Student_supervisor(student_id=students[2].id, supervisor_id=supervisors[1].id),
        Student_supervisor(student_id=students[3].id, supervisor_id=supervisors[2].id),
        Student_supervisor(student_id=students[4].id, supervisor_id=supervisors[3].id),
        Student_supervisor(student_id=students[4].id, supervisor_id=supervisors[4].id),
    ]
    db.session.add_all(student_supervisor)
    db.session.commit()
    print("tables seeded")
