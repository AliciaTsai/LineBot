# encoding: utf-8

from datetime import datetime


class InMemoryFakeDB:

    """
    Following is the recommended data storage format.
    However, you could always design your own format if you want.

        records = {
            'unique_id_xxx': [
                ('user_1', 'user_2', 70, 'dinner', datetime(2017, 5, 13, 12, 1, 57)),
                ('user_2', 'user_1', 70, 'dinner', datetime(2017, 5, 13, 17, 22, 6)),
            ],
            'unique_id_yyy': [
                ('B', 'A', 110, 'lunch', datetime(2017, 5, 13, 10, 21, 58)),
                ('B', 'A', 90, 'dinner', datetime(2017, 5, 13, 16, 53, 21)),
                ('C', 'A', 30, 'ps4', datetime(2017, 5, 13, 00, 43, 11)),
            ],
        }

        summary = {
            'unique_id_xxx': {
                ('user1', 'user2'): 0,
            }
            'unique_id_yyy': {
                ('A', 'B'): -200,  # A needs to give B $-200
                ('A', 'C'): -30,   # A needs to give C $-30
            }
        }

        #####################################################
        ### !!!! MUST SEE !!!! Below example is WRONG !!! ###
        #####################################################

        summary = {
            'unique_id_yyy': {
                ('A', 'C'): -30,
                ('C', 'A'): 30,    # DUPLICATE!!! SHOULDN'T EXIST!!!
            }
        }

        # Wrong Reason:
        #   You could only choose either ('A', 'C') or ('C', 'A') to be key.
        #   {('A', 'C'): -30} and {('C', 'A'): 30} represents the same meaning.
        #   Only one of {('A', 'C'): -30} and {('C', 'A'): 30} could exist.

        # Recommended Solution:
        #   You could sort the tuple (the two users' names) before making the
        #   tuple being a key.

    """

    records = {}
    summary = {}

    def write(self, unique_id, borrower, owner, money, note):
        # 1. Write these information to `records`.
        if unique_id not in self.records.keys():
            self.records[unique_id] = []
            self.records[unique_id].append((borrower, owner, money, note, datetime.now()))
        else:
            self.records[unique_id].append((borrower, owner, money, note, datetime.now()))

        # 2. Calculate the latest balance_number, and update the result in `summary`.
        balance_number = 0
        if unique_id not in self.summary.keys():
            self.summary[unique_id] = {}
            self.summary[unique_id][(borrower, owner)] = money
            balance_number = self.summary[unique_id][(borrower, owner)]
        else:
            if (borrower, owner) in self.summary[unique_id].keys():
                post_balance = self.summary[unique_id][(borrower, owner)]
                self.summary[unique_id][(borrower, owner)] = str(int(post_balance) + int(money))
                balance_number = self.summary[unique_id][(borrower, owner)]
            if (owner, borrower) in self.summary[unique_id].keys():
                post_balance = self.summary[unique_id][(borrower, owner)]
                self.summary[unique_id][(borrower, owner)] = str(int(post_balance) - int(money))
                balance_number = self.summary[unique_id][(owner, borrower)]

        # 3. Return the latest balance_number
        return borrower, owner, balance_number

    def get_all_summary(self, unique_id):
        # Return all people pairs' balance number.
        balance_records = []

        if unique_id not in self.summary.keys():
            return None
        else:
            for key in self.summary[unique_id].keys():
                tuple = (key[0], key[1], self.summary[unique_id][key])
                balance_records.append(tuple)
            return balance_records

    def get_recent_records(self, unique_id):
        # Return most recent 5 records.
        records = self.records[unique_id]
        return records[len(records)-5:]


import traceback
import sys
class PostgreDB:

    def __init__(self, db_conn):
        self.conn = db_conn
        print("Inside db:")
        print(self.conn)

    def write(self, unique_id, borrower, owner, money, note):
        try:
            self._write_records(unique_id, borrower, owner, money, note)
        except Exception as e:
            print("Error when writing records.")
            traceback.print_exc(file=sys.stdout)
            raise e

        try:
            result = self._write_summary(unique_id, borrower, owner, money)
        except Exception as e:
            print("Error when writing summary.")
            traceback.print_exc(file=sys.stdout)
            raise e

        return result

    def _write_records(self, unique_id, borrower, owner, money, note):
        """
        Append new record to table `records`.
        """
        cur = self.conn.cursor()
        cur.execute(


                # Fill in all the ____s. [TODO_DB]
                "INSERT INTO records (____, ____, ____, ____, ____, ____) VALUES (%s, %s, %s, %s, %s, %s)",
                (unique_id, ____, ____, ____, ____, datetime.today())
                )
        self.conn.commit()
        cur.close()

    def _write_summary(self, unique_id, borrower, owner, money):
        """
        Get `balance_number` from table `summary`.
        Calculate new `balance_number`, write back to table `summary`.
        """
        # Step 0 - Sort names. [TODO_DB]

        # Step 1 - Insert if not exists. Then update new value.
        cur = self.conn.cursor()
        cur.execute(
                # Fill in all the ____s. [TODO_DB]
                "INSERT INTO summary (____, ____, ____, ____) \
                        VALUES (____, ____, ____, ____) \
                        ON CONFLICT (____, ____, ____) DO NOTHING",
                (____, ____, ____, ____)
                )
        cur.execute(
                # Fill in all the ____s. [TODO_DB]
                "UPDATE summary \
                        SET ____ = ____ + ____ \
                        WHERE ____ = %s and ____ = %s and ____ = %s \
                        RETURNING balance_number",
                (____, ____, ____, ____)
                )
        self.conn.commit()

        balance_number = cur.fetchone()[0]
        cur.close()

        # Step 2 - return new balance_number and people orders.
        return (person1, person2, balance_number)

    def get_all_summary(self, unique_id):
        cur = self.conn.cursor()
        # Fill in all the ____s. [TODO_DB]
        cur.execute(
                "SELECT ____, ____, ____ FROM ____ WHERE ____ = ____",
                (____, )
                )
        for ____, ____, ____ in cur.fetchall():
            yield (____, ____, ____)
        cur.close()

    def get_recent_records(self, unique_id):
        cur = self.conn.cursor()
        cur.execute(
                # Fill in all the ____s. [TODO_DB]
                "SELECT ____, ____, ____, ____, ____ FROM ____ WHERE ____ = ____ ORDER BY ____ DESC LIMIT ____",
                (____, )
                )
        records = cur.fetchall()
        cur.close()
        return records


class DataManager:
    def __init__(self, conn=None):
        if not conn:
            self.db = InMemoryFakeDB()
        else:
            self.db = PostgreDB(conn)

    def write(self, unique_id, borrower, owner, money, note):
        return self.db.write(unique_id, borrower, owner, money, note)

    def get_all_summary(self, unique_id):
        return self.db.get_all_summary(unique_id)

    def get_recent_records(self, unique_id):
        return self.db.get_recent_records(unique_id)
