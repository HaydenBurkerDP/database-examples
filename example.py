import sqlite3
import csv

connection = sqlite3.connect("example.db")

cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Examples (
    example_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)""")


def create_example(name):
    cursor.execute("INSERT INTO Examples (name) VALUES (?)", [name])
    connection.commit()


def read_all_examples():
    return cursor.execute("SELECT * FROM Examples").fetchall()


def read_example(example_id):
    return cursor.execute("SELECT * FROM Examples WHERE example_id = ?", [example_id]).fetchone()


def update_example(example_id, name):
    cursor.execute("UPDATE Examples SET name = ? WHERE example_id = ?", [name, example_id])
    connection.commit()


def delete_example(example_id):
    cursor.execute("DELETE FROM Examples WHERE example_id = ?", [example_id])
    connection.commit()


def create_examples_from_csv(file_name):
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            name = row[0]
            create_example(name)


# create_example("Testing!")

# create_examples_from_csv("examples.csv")

# update_example(2, "Testing 1")
# update_example(2, "Testing 2")
# update_example(2, "Testing 3")

# delete_example(3)

# print(read_example(1))
# print(read_example(2))
# print(read_example(3))

# print(read_all_examples())
