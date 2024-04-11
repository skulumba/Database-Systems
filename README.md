
### Researcher’s Dashboard

This is a dashboard for academic researchers, which provides various features such as finding publications by keyword, finding the top faculty members by number of publications and position, adding and deleting a keyword from the database, and finding faculty members associated with a keyword.

#### Installation

To use this app, you must have Python 3.x installed on your computer. You can install the required dependencies by running the following command in your terminal:

```bash
pip install -r requirements.txt
```
To run the app, simply execute the following command in your terminal:
```bash
python app.py
```
This will start the server and launch the app in your default web browser.

You have to create a new account to access the dashboard.

### Features
- Find Publications by Keyword

This feature allows the user to find the top 5 publications based on a keyword. The user can enter a keyword in the input field and click the "Find" button to see the search results. The search results are displayed in a table, and a bar chart showing the number of citations for the top 5 publications is displayed.

- Find Top Faculty Members by Number of Publications and Position

This feature allows the user to find the top 5 faculty members based on the number of publications and their position at a specific university. The user can enter the name of the university in the input field and click the "Find" button to see the search results. The search results are displayed in a table, and a pie chart showing the distribution of faculty members by position is displayed.

```sql
-- View to count faculty positions by university
CREATE VIEW faculty_position_count AS 
SELECT 
    u.name AS university_name, 
    f.position, 
    COUNT(*) AS count 
FROM 
    faculty f 
INNER JOIN 
    university u ON f.university_id = u.id 
GROUP BY 
    u.name, 
    f.position;
```
| Field           | Type         | Null | Key | Default | Extra |
|-----------------|--------------|------|-----|---------|-------|
| university_name | varchar(512) | YES  |     | NULL    |       |
| position        | varchar(512) | YES  |     | NULL    |       |
| count           | bigint       | NO   |     | 0       |       |


-  Add a Keyword to the Database

This feature allows the user to add a new keyword to the database. The user can enter the ID and name of the keyword in the input fields and click the "Add" button to add the keyword to the database. The keyword is then displayed in a table.
![image](https://github.com/skulumba/Database-Systems/assets/75015106/d1539b90-db79-4896-a320-1854340422da)

| ROUTINE_NAME            | ROUTINE_TYPE |
|-------------------------|--------------|
| get_last_three_keywords | PROCEDURE    |


- Delete a Keyword from the Database

This feature allows the user to delete a keyword from the database. The user can enter the ID of the keyword in the input field and click the "Delete" button to delete the keyword from the database. A message is displayed indicating whether the keyword was successfully deleted or not. Also  delete triggers  keyword_delete_trigger which creates a new row in the keyword_log table for each deleted row in the keyword table, with the id and name fields from the deleted row, and a timestamp for when the row was deleted

```sql
-- Trigger to log deleted keywords
CREATE TRIGGER keyword_delete_trigger AFTER DELETE ON keyword FOR EACH ROW 
BEGIN 
    INSERT INTO keyword_log (id, name, deleted_at) VALUES (OLD.id, OLD.name, NOW()); 
END;

-- Table to keep track of deleted keywords
CREATE TABLE keyword_log (
    id INT NOT NULL,
    name VARCHAR(512),
    deleted_at TIMESTAMP
);
```

![image](https://github.com/skulumba/Database-Systems/assets/75015106/a9d46e72-6724-41f0-9eb7-5220f937439a)


| TRIGGER_NAME          | EVENT_OBJECT_TABLE | ACTION_TIMING | ACTION_STATEMENT                                                                                   |
|-----------------------|--------------------|---------------|----------------------------------------------------------------------------------------------------|
| keyword_delete_trigger| keyword            | AFTER         | BEGIN<br>INSERT INTO keyword_log (id, name, deleted_at)<br>VALUES (OLD.id, OLD.name, NOW());<br>END |


- View Faculty Members with the Highest Number of Publications

This feature allows the user to find the top faculty members with the highest number of publications. The search results are displayed in a bar chart.

- Find top Faculty Members Associated with a Keyword

This feature allows the user to find the faculty members associated with a specific keyword. The user can enter a keyword in the input field and click the "Find" button to see the search results. The search results are displayed in a pie chart.

[Watch the Demo Video](https://mediaspace.illinois.edu/media/t/1_zxaswef3)

