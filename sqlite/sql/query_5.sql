--Знайти які курси читає певний викладач.
select t.First_Name, t.Last_Name, s.Subject_Name
from Teachers t
join Subjects s on s.Teacher_ID = t.Teacher_ID