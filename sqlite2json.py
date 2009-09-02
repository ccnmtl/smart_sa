from  pysqlite2 import dbapi2 as sqlite
import json

connection = sqlite.connect('webappsstore1.sqlite')
cursor = connection.cursor()
cursor.execute("SELECT key,value FROM webappsstore WHERE key LIKE 'USER%'")

json_blob = json.dumps(dict([(r[0],r[1]) for r in cursor.fetchall()]))
print "openjson(%s);" % json_blob


