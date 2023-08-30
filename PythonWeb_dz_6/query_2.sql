-- Знайти студента із найвищим середнім балом з певного предмета.
SELECT stu.student, ROUND(AVG(eval.evaluation), 2) as eval_i
FROM evaluations as eval
LEFT JOIN students as stu ON eval.student_id = stu.id
WHERE eval.subject_id = 8
GROUP BY stu.student
ORDER BY eval_i DESC
LIMIT 1;