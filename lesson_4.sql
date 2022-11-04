/*********************************************
Quiz:  Your First Subquery
*********************************************/

/* Question 1:
A - Find the number of events that occur for each day for each channel.
B - Now creat a subquery that simply provides all of the data from your first query.
C - Now find the average number of events for each channel. Since you broke out by day earlier , this is giving you an average per day. */

/* inline subquery */
SELECT channel,
       AVG(event_count) AS avg_event_count
FROM (SELECT DATE_TRUNC('day', w.occurred_at) AS day,
             w.channel,
             COUNT(*) AS event_count
      FROM web_events w
      GROUP BY 1, 2) sub
GROUP BY 1
ORDER BY 2 DESC;

/*********************************************
Quiz: More Subquery Practice
*********************************************/

/* Question 1: Use DATE_TRUNC to pull month-level information about the first order ever placed in the orders table. */
SELECT DATE_TRUNC('month', MIN(occurred_at)) AS earliest_month
FROM orders;

/* Question 2: Use the result of the previous query to find only the orders that took place in the same month and year as the first order, and then pull the average for each type of paper qty in this month */
SELECT AVG(standard_qty) avg_standard_qty, 
       AVG(poster_qty) avg_poster_qty,
       AVG(gloss_qty) avg_gloss_qty,
       SUM(total_amt_usd) total_sales_usd
FROM orders
WHERE DATE_TRUNC('month', occurred_at) = (
        SELECT DATE_TRUNC('month', MIN(occurred_at)) AS earliest_month
        FROM orders);

/*********************************************
Quiz: SIMPLE vs CORRELATED - Examples
*********************************************/
/*  */

/* SIMPLE example:
WITH dept_average AS 
  (SELECT dept, AVG(salary) AS avg_dept_salary
   FROM employee
   GROUP BY employee.dept
  )
SELECT E.eid, E.ename, D.avg_dept_salary
FROM employee E
JOIN dept.average D
ON E.dept = D.dept
WHERE E.salary > D.avg_dept_salary
*/

/* CORRELATED example:
SELECT employee_id,
       name
FROM employees_db emp
WHERE salary > 
      (SELECT AVG(salary)
       FROM employees_db
       WHERE department = emp.department
      );
*/

/* Example of when to use a CORRELATED subquery - inner query dependent on outer query because filter changes based on outer query data :
SELECT first_name, last_name, GPA, university
 FROM student_db outer_db
 WHERE GPA >
                (SELECT AVG(GPA)
                 FROM student_db
                 WHERE university = outer_db.university);
*/

/*********************************************
Quiz: Subquery Example - Challenge
*********************************************/

/* Question 1: What is the top channel used by each account to market products? */

SELECT a.name account, w.channel channel, COUNT(*) AS channel_uses
FROM orders o
JOIN accounts a
ON a.id = o.account_id
JOIN web_events w
ON a.id = w.account_id
GROUP BY 1, 2
ORDER BY 3 DESC;