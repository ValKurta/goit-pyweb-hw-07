--Знайти 5 студентів із найбільшим середнім балом з усіх предметів
with a as (
	select s.Student_ID, s.First_Name, s.Last_Name, s.Group_ID, s.Date_Of_Birth, avg(cast(g.Grade as int)) as Grade
	from Students s
	join Grades g
	on g.Student_ID = s.Student_ID
	group by s.Student_ID, s.First_Name, s.Last_Name, s.Group_ID, s.Date_Of_Birth)
select *
from a
order by Grade desc
limit 5