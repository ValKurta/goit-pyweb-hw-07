--Знайти список курсів, які відвідує студент.
select distinct s.Subject_Name
from Subjects s
join Grades g on g.Subject_ID =s.Subject_ID
join Students s2 on S2.Student_ID = g.Student_ID
where g.Student_ID = (select Student_id from Students s3 order by Student_id desc limit 1)
order by s.Subject_Name