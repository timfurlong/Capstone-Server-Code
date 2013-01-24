import sqlite3
import os
from config import config
import datetime
from pprint import pprint

class DB:
	'''This module controls all interaction with the SQLite database.'''

	DB_PATH = os.path.join( config['rootPath'], 'CapstoneDatabase.db')

	def createAllTables(self):
		conn = sqlite3.connect( self.DB_PATH,
							detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		c = conn.cursor()

		c.execute("""CREATE TABLE MotionVectors
						(id INTEGER PRIMARY KEY, time TIMESTAMP, camera_id NUMERIC,
						relX NUMERIC, relY NUMERIC, magX NUMERIC, magY NUMERIC);
					""")

		c.execute("""CREATE TABLE StitchedImages
						(id INTEGER PRIMARY KEY, time TIMESTAMP, image BLOB);
					""")

		c.execute("""CREATE TABLE cameras
						(id INTEGER PRIMARY KEY, geotag TEXT);
					""")

		c.execute("""CREATE TABLE ongridSensors
						(id INTEGER PRIMARY KEY, geotag TEXT);
					""")

		conn.commit()
		conn.close()

	def printTableData(self, tableName):
		conn = sqlite3.connect( self.DB_PATH,
							detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		c = conn.cursor()
		c.execute("SELECT * FROM %s" % tableName ) # Cannot use ? for column or table names
		data = c.fetchall()

		print '# of rows = %d' % len(data)
		pprint( data )

		conn.close()

	# =======================================
	# ======== DB Write methods =============
	# =======================================

	def writePowerData(self, power, geotag, timetag):
		# The detect_types keyword param tells sqlite to convert datetime objs automatically
		conn = sqlite3.connect( self.DB_PATH,
							detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		c = conn.cursor()

		# (id INTEGER, time TEXT ,
		#  geotag TEXT , power NUMERIC)
		c.execute(
				"""INSERT INTO PowerData (power, time, geotag)
					VALUES (?,?,?)
					""" , (power, timetag, geotag) )
		conn.commit()
		conn.close()

	def addCamera(self, geotag):
		conn = sqlite3.connect( self.DB_PATH,
							detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		c = conn.cursor()

		c.execute(
				"""INSERT INTO cameras(geotag)
					VALUES (?)
					""" , (geotag,) )

		conn.commit()
		conn.close()

	def addOnGridSensor(self, geotag):
		conn = sqlite3.connect( self.DB_PATH,
							detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
		c = conn.cursor()

		c.execute(
				"""INSERT INTO ongridSensors(geotag)
					VALUES (?)
					""" , (geotag,) )

		conn.commit()
		conn.close()



if __name__ == '__main__':
	timetag = datetime.datetime.now()
	geotag  = 'TEST_GEOTAG'

	db = DB()
	db.addOnGridSensor(geotag)
	db.printTableData('ongridSensors')


"""
# this row factory makes the results objects accessible both by index
# and by column name
self.conn.row_factory = sqlite3.Row


"""


