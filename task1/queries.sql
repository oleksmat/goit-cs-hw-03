-- 1. Get all tasks for a specific user
SELECT *
FROM tasks
WHERE user_id = ?;
-- Replace ? with desired user_id

-- 2. Select tasks with specific status using subquery
SELECT *
FROM tasks
WHERE status_id IN (SELECT status_id FROM status WHERE name = 'new');

-- 3. Update status of specific task
UPDATE tasks
SET status_id = (SELECT status_id FROM status WHERE name = 'in progress')
WHERE id = ?;
-- Replace ? with desired task_id

-- 4. Get users with no tasks
SELECT *
FROM users
WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);

-- 5. Add new task for specific user
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('New Task', 'Task Description', (SELECT id FROM status WHERE name = 'new'), 1);

-- 6. Get all incomplete tasks
SELECT *
FROM tasks
WHERE status_id != (SELECT id FROM status WHERE name = 'completed');

-- 7. Delete specific task
DELETE
FROM tasks
WHERE id = ?;
-- Replace ? with desired task_id

-- 8. Find users with specific email pattern
SELECT *
FROM users
WHERE email LIKE ?;
-- Replace with desired email pattern, ex '%@gmail.com'

-- 9. Update username
UPDATE users
SET fullname = 'New Name'
WHERE id = ?;
-- Replace 1 with desired user_id

-- 10. Count tasks by status
SELECT (SELECT name FROM status where id = status_id) as status, COUNT(*) as task_count
FROM tasks
GROUP BY status_id;

-- 11. Get tasks for users with specific email domain
SELECT t.*
FROM tasks t
         INNER JOIN users u ON t.user_id = u.id
WHERE u.email LIKE ?;
-- Replace ? with desired email pattern, ex '%@example.com'

-- 12. Get tasks without description
SELECT *
FROM tasks
WHERE description = '';

-- 13. Select users and their in-progress tasks
SELECT u.fullname, t.title
FROM users u
         INNER JOIN tasks t ON u.id = t.user_id
WHERE t.status_id = (SELECT id FROM status where name = 'in progress');

-- 14. Get users and their task count
SELECT u.fullname, COUNT(t.id) as task_count
FROM users u
         LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id, u.fullname;