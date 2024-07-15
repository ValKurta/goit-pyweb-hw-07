--Середній бал, який певний викладач ставить певному студентові.
select t.First_Name||' '||t.Last_Name as Teacher_Full_Name, s2.First_Name||' '||s2.Last_Name as Student_Full_Name, cast(avg(cast(g.Grade as integer)) * 10 as integer) / 10.0 as AverageGrade
from Grades g
left join Teachers t on t.Teacher_ID = g.Subject_ID
left join Subjects s on s.Teacher_ID = t.Teacher_ID
left join Students s2 on g.Student_ID = s2.Student_ID
group by t.First_Name, t.Last_Name, s2.First_Name, s2.Last_Name
order by t.Last_Name, t.First_Name, AverageGrade desc