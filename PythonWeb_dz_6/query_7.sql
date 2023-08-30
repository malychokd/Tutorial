-- Знайти оцінки студентів в окремій групі з певного предмета.
SELECT stu.student, eval.evaluation
FROM evaluations as eval
LEFT JOIN students as stu ON eval.student_id = stu.id
WHERE stu.group_id = 3 AND eval.subject_id = 8;