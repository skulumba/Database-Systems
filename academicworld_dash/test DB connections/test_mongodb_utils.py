from mongodb_utils import connect_to_database, execute_query

# Test connect_to_database
db = connect_to_database()
print(db)

# check publication
collist = db.list_collection_names()
if "publications" in collist:
  print("Yes Publications exists.")
# check for faculty
if "faculty" in collist:
  print("Yes faculty exists.")

# Test execute_query
result = execute_query({"position": "Assistant Professor"})
print(f'The number of Assistant Professors is : {result}')

