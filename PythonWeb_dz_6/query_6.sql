-- Знайти список студентів у певній групі.
SELECT stu.student
FROM students as stu
WHERE stu.group_id = 3;