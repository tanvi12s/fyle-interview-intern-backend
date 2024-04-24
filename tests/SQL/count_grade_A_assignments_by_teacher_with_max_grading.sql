-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH graded_assignments AS (
    SELECT teacher_id, COUNT(*) AS no_of_a
    FROM assignments
    WHERE grade = 'A'
    GROUP BY teacher_id
)
SELECT no_of_a
FROM graded_assignments
WHERE no_of_a = (SELECT MAX(no_of_a) FROM graded_assignments);
