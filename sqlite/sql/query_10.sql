--Список курсів, які певному студенту читає певний викладач.
select distinct s.Subject_Name
from Grades g
left join Teachers t on t.Teacher_ID = g.Subject_ID
left join Subjects s on s.Teacher_ID = t.Teacher_ID
left join Students s2 on g.Student_ID = s2.Student_ID
where
s2.First_Name||' '||s2.Last_Name = 'Katherine Moore'
and  t.First_Name||' '||t.Last_Name = 'Rebekah Cross'