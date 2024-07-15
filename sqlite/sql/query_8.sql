--Знайти середній бал, який ставить певний викладач зі своїх предметів.
select t.First_Name || ' ' || t.Last_Name as Full_Name, avg(cast(g.Grade as integer)) as AverageGrade
from Teachers t
join Subjects s on s.Teacher_id  = t.Teacher_id
left join Grades g on g.Subject_ID = s.Subject_ID
group by t.First_Name || ' ' || t.Last_Name
order by AverageGrade desc