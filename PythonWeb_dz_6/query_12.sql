-- Оцінки студентів у певній групі з певного предмета на останньому занятті.
SELECT stu.id, stu.student AS student_name, sub.subject_name AS subject_name, eval.evaluation AS student_eval, eval.data_eval
FROM students as stu
LEFT JOIN group_students as gro ON stu.group_id = gro.id
LEFT JOIN evaluations as eval ON stu.id = eval.student_id
LEFT JOIN subjects as sub ON eval.subject_id = sub.id
WHERE gro.id = 1
  AND sub.id = 1
  AND eval.data_eval = (SELECT MAX(data_eval) FROM evaluations WHERE student_id = stu.id AND subject_id = sub.id)
ORDER BY student_name;