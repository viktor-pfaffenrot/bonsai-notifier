#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 01:22:28 2022

Author: Viktor Pfaffenrot


This class creates a bonsai with an id, a name and action attributes 
namely when to next fertilize, when was the last pruning, the last repotting and the last wiring.
"""

from dataclasses import dataclass, field
import bonsai_database as bonsai_db
import os


@dataclass()
class bonsai:
    r"""
    Setters of the action attributes

    .. automethod:: set_next_fertilize
    .. automethod:: set_last_pruning
    .. automethod:: set_last_repot
    .. automethod:: set_last_wiring

    Remaining:
    """

    all = []  #:keeps track of all the created instances
    treeid: int = 1
    name: str = "bonsai"
    next_fertilize: str = "Not Yet"
    last_pruning: str = "Not Yet"
    last_repot: str = "Not Yet"
    last_wiring: str = "Not Yet"
    info: str = ""

    def __post_init__(self):
        bonsai.all.append(self)

    # =============================================================================
    #         for field in fields(self):
    #             if not isinstance(field.default, dataclasses._MISSING_TYPE) and getattr(self, field.name) is None:
    #                 setattr(self, field.name, field.default)
    # =============================================================================

    def __hash__(self):
        return hash(tuple(self))

    # @staticmethod
    def initiate_database(db_file: str):
        r"""
        This method initializes the bonsai database if not already existent. Calls ``bonsai_database.initialize_table()``
        """
        conn = bonsai_db.create_connection(db_file)
        bonsai_db.initialize_table(conn)

    @classmethod
    def load_database(cls, db_file: str):
        r"""
        Loads the bonsai database. Calls ``bonsai_database.load_database()``

        :return: List of bonsai objects.
        """
        conn = bonsai_db.create_connection(db_file)
        db = bonsai_db.load_database(conn)
        mytrees = []
        for item in db:
            mytrees.append(
                bonsai(
                    treeid=item[0],
                    name=item[1],
                    next_fertilize=item[2],
                    last_pruning=item[3],
                    last_repot=item[4],
                    last_wiring=item[5],
                )
            )
        return mytrees

    # @staticmethod
    def update_database(self, db_file: str, add: bool):
        r"""
        Updates the bonsai database. Calls ``bonsai_database.add_record()`` or ``bonsai_database.remove_record()`` depending on add flag
        """
        conn = bonsai_db.create_connection(db_file)

        if add:
            bonsai_db.add_record(conn, self)
        else:
            bonsai_db.remove_record(conn, self)

    def set_next_fertilize(self, next_fertilize: str):
        self.next_fertilize = next_fertilize

    def set_last_pruning(self, last_pruning: str):
        self.last_pruning = last_pruning

    def set_last_repot(self, last_repot: str):
        self.last_repot = last_repot

    def set_last_wiring(self, last_wiring: str):
        self.last_wiring = last_wiring

    def set_info(self, db_file: str):
        db_path = os.path.split(db_file)
        db_path = db_path[0]
        self.info = db_path + "/" + self.name.replace(" ", "_") + ".json"
