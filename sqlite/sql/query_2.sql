--Знайти студента із найвищим середнім балом з певного предмета.
with a as(
	select
	Student_ID
	,Subject_ID
	,avg(cast(Grade as int)) as Average_Grade
	from Grades
	group by Student_ID, Subject_ID)
, b as (
	select *
	, dense_rank() over (partition by Subject_ID order by Average_Grade desc) as rn
	from a)
select s2.Subject_Name, b.Average_Grade, s.First_Name,s.Last_Name, g.Group_Name
from b
left join Students s on b.Student_id = s. Student_ID
left join Subjects s2 on b.Subject_ID = s2.Subject_ID
left join Groups g on g.Group_ID = s.Group_ID
where rn = 1