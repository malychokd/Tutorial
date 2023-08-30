-- Знайти середній бал, який ставить певний викладач зі своїх предметів.
SELECT teach.teacher, ROUND(AVG(eval.evaluation), 2) as eval_i
FROM evaluations as eval
LEFT JOIN subjects as sub ON eval.subject_id = sub.id
LEFT JOIN teachers as teach ON sub.teacher_id = teach.id
WHERE sub.teacher_id = 5
GROUP BY teach.teacher;