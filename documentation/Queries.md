The course requires these...
===========================

Check out ```application/help.py```.

Deletion of a name with id 1:
```
DELETE FROM name WHERE id = 1;
```

Insertion of a new name for user whose id is 1:
```
INSERT INTO name (name, user_id) VALUES ('Pekka', 1);
```

Updating name of user with id 1:
```
UPDATE account
SET name = "Uusi nimi"
WHERE id = 1;
```