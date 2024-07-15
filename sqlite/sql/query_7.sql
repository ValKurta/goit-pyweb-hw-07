--Знайти оцінки студентів у окремій групі з певного предмета.
Select
g2.Group_Name
,s2.Subject_Name
,s.First_Name || ' ' || s.Last_Name as Full_Name
,cast(g.Grade as integer) Grade
from Grades g
join Students s on s.Student_ID = g.Student_ID
join Groups g2 on g2.Group_ID =s.Group_ID
join Subjects s2 on s2.Subject_ID  = g.Subject_ID
where
g2.Group_Name = (select Group_Name from Groups g3 limit 1)
and s2.Subject_Name = (select Subject_Name from Subjects s3 limit 1)
order by s.Last_Name