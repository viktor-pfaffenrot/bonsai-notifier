#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 23:22:43 2022

Author: Viktor Pfaffenrot


Collection of functions to maintain a small SQL database of the bonsai
"""

# DATATYPES
# NULL
# INTEGER
# REAL
# TEXT
# BLOB

import sqlite3


def create_connection(db_file: str):
    """
    Creates a connection to the bonsai database.

    :return: Connection object.
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


def initialize_table(conn):
    r"""
    Initializes the database if not already existent

    :return: True
    """
    cur = conn.cursor()

    # check if table exists and if not, create one
    listOfTables = cur.execute(
        """SELECT name FROM sqlite_master WHERE type='table'
      AND name='bonsai'; """
    ).fetchall()

    if listOfTables == []:
        # create table
        cur.execute(
            """CREATE TABLE bonsai (
            treeid INTEGER,
            name TEXT,
            next_fertilize TEXT,
            last_pruning TEXT,
            last_repot TEXT,
            last_wiring TEXT
        )"""
        )

        bonsai = [
            [0, "Ficus", "22.03.2023", "29.12.2022", "Not Yet", "27.11.2022"],
            [1, "Fukientea", "23.03.2023", "04.02.2023", "Not Yet", "Not Yet"],
            [
                2,
                "Chinese Elm",
                "17.03.2023",
                "Not Yet",
                "24.09.2022",
                "Not Yet",
            ],
            [
                3,
                "Chinese Pivet",
                "17.03.2023",
                "28.01.2023",
                "Not Yet",
                "Not Yet",
            ],
            [
                4,
                "Ficus Benj. Starl.",
                "10.03.2023",
                "Not Yet",
                "Not Yet",
                "Not Yet",
            ],
            [5, "Old Ficus", "20.03.2023", "Not Yet", "Not Yet", "Not Yet"],
        ]

        cur.executemany("INSERT INTO bonsai VALUES(?,?,?,?,?,?)", bonsai)
    else:
        pass

    conn.commit()
    return True


def load_database(conn):
    r"""
    Loads the latest records for each bonsai in the database

    :return: list of tuples containing the attributes of each instance of the bonsai class
    """
    cur = conn.cursor()
    table = cur.execute(
        """SELECT * FROM (SELECT * from bonsai ORDER BY rowid DESC) GROUP BY treeid;"""
    ).fetchall()

    return table


# add record defines as tuple
def add_record(conn, new_record):
    r"""
    Adds a record to the database

    :return: True
    """
    sql = "INSERT INTO bonsai VALUES(?,?,?,?,?,?)"
    new_record = [
        new_record.treeid,
        new_record.name,
        new_record.next_fertilize,
        new_record.last_pruning,
        new_record.last_repot,
        new_record.last_wiring,
    ]
    cur = conn.cursor()
    cur.execute(sql, new_record)

    conn.commit()
    return True


# remove record
def remove_record(conn, remove_record):
    r"""
    Removes a record to the database

    :return: True
    """
    sql = "DELETE from bonsai WHERE treeid = ?"

    cur = conn.cursor()
    cur.execute(sql, (remove_record.treeid,))

    conn.commit()
    return True
