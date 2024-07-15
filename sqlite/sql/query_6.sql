--Знайти список студентів у певній групі.
select g.Group_Name, s.*
from Groups g
join Students s on s.Group_ID =g.Group_ID
where g.Group_name='Young-Hardin'
order by s.Last_Name