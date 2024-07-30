from sqlalchemy import create_engine, MetaData, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

import csv

echo = False

engine = create_engine("sqlite:///example_sqlalchemy.db", echo=echo)

metadata_obj = MetaData()
Base = declarative_base(metadata=metadata_obj)

Session = sessionmaker(bind=engine)
session = Session()


class Examples(Base):
    __tablename__ = "Examples"

    example_id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str((self.example_id, self.name))


Base.metadata.create_all(engine)


def create_example(name):
    example = Examples(name)

    session.add(example)
    session.commit()


def read_all_examples():
    return session.query(Examples).all()


def read_example(example_id):
    return session.query(Examples).filter(Examples.example_id == example_id).first()


def update_example(example_id, name):
    example = read_example(example_id)

    if not example:
        return

    example.name = name
    session.commit()


def delete_example(example_id):
    example = read_example(example_id)

    if not example:
        return

    session.delete(example)
    session.commit()


def create_examples_from_csv(file_name):
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            name = row[0]
            create_example(name)


# create_example("Testing")

# create_examples_from_csv("examples.csv")

# update_example(1, "Testing 1")
# update_example(2, "Testing 2")
# update_example(3, "Testing 3")

# delete_example(3)

# print(read_example(1))
# print(read_example(2))
# print(read_example(3))

# print(read_all_examples())
