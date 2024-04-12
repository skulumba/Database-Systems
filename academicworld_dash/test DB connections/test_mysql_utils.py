from mysql_utils import connect_to_database, execute_query, update_database

# Test connect_to_database
conn = connect_to_database()
print(conn)

# Test execute_query
query = "SELECT COUNT(*) AS num_assistant_professors\
        FROM faculty\
        WHERE position = 'Assistant Professor'"

result = execute_query(query)
print(f'The number of Assistant Profess0rs is : {result}')

# Test update_database
#query = "UPDATE faculty SET name='' WHERE id= "
#update_database(query)
