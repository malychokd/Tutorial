-- Середній бал, який певний викладач ставить певному студентові.
SELECT ROUND(AVG(eval.evaluation), 2) as eval_i
FROM evaluations as eval
LEFT JOIN subjects as sub ON eval.subject_id = sub.id
WHERE eval.student_id = 35 AND sub.teacher_id = 4;