--Знайти середній бал у групах з певного предмета.
select
g2.Group_Name
,s2.Subject_Name
,cast(avg(cast(Grade as integer)) * 10 as integer) / 10.0 as AverageGrade
from Grades g
left join Students s on g.Student_ID = g.Student_ID
left join Groups g2 on s.Group_ID = g2.Group_ID
left join Subjects s2 on s2.Subject_ID = g.Subject_ID
group by
g2.Group_Name
,s2.Subject_Name
order by
g2.Group_Name
,s2.Subject_Name