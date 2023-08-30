-- Знайти список курсів, які відвідує студент.
SELECT sub.subject_name
FROM evaluations as eval
LEFT JOIN subjects as sub ON eval.subject_id = sub.id
WHERE eval.student_id = 1
GROUP BY sub.subject_name;