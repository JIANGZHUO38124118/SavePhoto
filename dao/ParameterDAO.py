# # dao/ParameterDAO.py

# import sqlite3
# from entity.Parameter import Parameter


# class ParameterDAO:

#     def __init__(self):

#         self.conn = sqlite3.connect(
#             "database/photo.db"
#         )

#     def getParameter(self):

#         cursor = self.conn.cursor()

#         cursor.execute(
#             '''
#             SELECT *
#             FROM parameter
#             LIMIT 1
#             '''
#         )

#         row = cursor.fetchone()

#         return Parameter(
#             row[1],
#             row[2]
#         )