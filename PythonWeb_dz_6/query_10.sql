-- Список курсів, які певному студенту читає певний викладач.
SELECT sub.subject_name
FROM evaluations as eval
LEFT JOIN subjects as sub ON eval.subject_id = sub.id
WHERE eval.student_id = 50 AND sub.teacher_id = 5
GROUP BY sub.subject_name;