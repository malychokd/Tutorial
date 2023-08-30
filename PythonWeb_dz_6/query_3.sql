-- Знайти середній бал у групах з певного предмета.
SELECT gro.group_name, ROUND(AVG(eval.evaluation), 2) as eval_i
FROM evaluations as eval
LEFT JOIN students as stu ON eval.student_id = stu.id
LEFT JOIN group_students as gro ON stu.group_id = gro.id
WHERE eval.subject_id = 8
GROUP BY gro.group_name;