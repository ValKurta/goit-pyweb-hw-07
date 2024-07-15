--Оцінки студентів у певній групі з певного предмета на останньому занятті.
with a as (
    select *
    ,row_number() over (partition by Student_id,Subject_id order by Date_Received desc) as rn
    from Grades nolock)
select g.Group_Name, s2.Subject_Name, s.First_Name||' '||s.Last_Name as Student_Full_Name, a.Date_Received
from a
join Students s on s.Student_ID =a.Student_ID
join Groups g on g.Group_ID = s.Group_ID
join Subjects s2 on s2.Subject_ID = g.Group_ID
where rn = 1
and g.Group_ID = (select Group_ID from Groups nolock limit 1)
and a.Subject_id = (select Subject_id from Subjects nolock limit 1)