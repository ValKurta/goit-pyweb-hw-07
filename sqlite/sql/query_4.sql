--Знайти середній бал на потоці (по всій таблиці оцінок).
select avg(cast(Grade as integer)) AverageGrade from Grades nolock