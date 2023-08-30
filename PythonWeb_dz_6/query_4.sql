-- Знайти середній бал на потоці (по всій таблиці оцінок).
SELECT ROUND(AVG(eval.evaluation), 2) as eval_i
FROM evaluations as eval;