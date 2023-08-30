-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT stu.student, ROUND(AVG(eval.evaluation), 2) as eval_i
FROM evaluations as eval
LEFT JOIN students as stu ON eval.student_id = stu.id
GROUP BY stu.student
ORDER BY eval_i DESC
LIMIT 5;