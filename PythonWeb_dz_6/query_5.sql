-- Знайти, які курси читає певний викладач.
SELECT sub.subject_name
FROM subjects as sub
WHERE sub.teacher_id = 5;