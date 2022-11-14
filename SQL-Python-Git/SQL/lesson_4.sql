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
FROM accounts a
JOIN web_events w
ON a.id = w.account_id
GROUP BY 1, 2
ORDER BY 3 DESC;

SELECT account, MAX(channel_uses) count_max
FROM (SELECT a.name account, w.channel channel, COUNT(*) AS channel_uses
      FROM accounts a
      JOIN web_events w
      ON a.id = w.account_id
      GROUP BY 1, 2) Table1
GROUP BY 1
ORDER BY 1;

/* Question 2: How often was that same channel used? */

SELECT t3.name, t3.channel, t3.ct
FROM (SELECT a.name, w.channel, COUNT(*) AS ct
      FROM accounts a
      JOIN web_events w
      ON a.id = w.account_id
      GROUP BY 1, 2) t3
JOIN (SELECT t1.name, MAX(ct) AS max_ct
      FROM (SELECT a.name, w.channel, COUNT(*) AS ct
            FROM accounts a
            JOIN web_events w
            ON a.id = w.account_id
            GROUP BY 1, 2) t1
      GROUP BY 1) t2
ON t3.name = t2.name AND t2.max_ct = t3.ct
ORDER BY 1;

/*********************************************
Quiz: Subquery Quiz
*********************************************/

/* Question 1: Provide the name of the sales_rep in each region with the largest amount of total_amt_usd sales. */
SELECT t3.region_id, t3.name, t2.max_sales
FROM (SELECT s.name, s.region_id, SUM(o.total_amt_usd) rep_total_sales
      FROM sales_reps s
      JOIN accounts a ON s.id = a.sales_rep_id
      JOIN orders o ON a.id = o.account_id
      GROUP BY 1, 2) t3
JOIN (SELECT t1.region_id, MAX(t1.rep_total_sales) max_sales
      FROM (SELECT s.name, s.region_id, SUM(o.total_amt_usd) rep_total_sales
            FROM sales_reps s
            JOIN accounts a ON s.id = a.sales_rep_id
            JOIN orders o ON a.id = o.account_id
            GROUP BY 1, 2) t1
      GROUP BY 1) t2
ON t2.region_id = t3.region_id AND t3.rep_total_sales = max_sales
ORDER BY 1;

/* Question 2: For the region with the largest (sum) of sales total_amt_usd, how many total (count) orders were placed? */
SELECT r.name, COUNT(*) num_orders
FROM region r
JOIN sales_reps s
ON r.id = s.region_id
JOIN accounts a
ON s.id = a.sales_rep_id
JOIN orders o
ON a.id = o.account_id
GROUP BY 1
HAVING SUM(o.total_amt_usd) = (
      SELECT MAX(t1.sum_total_usd)
      FROM (SELECT r.id, r.name, SUM(o.total_amt_usd) sum_total_usd
            FROM region r
            JOIN sales_reps s
            ON r.id = s.region_id
            JOIN accounts a
            ON s.id = a.sales_rep_id
            JOIN orders o
            ON a.id = o.account_id
            GROUP BY 1, 2) t1);

/* Question 3: How many accounts had more total purchases than the account name which has bought the most standard_qty paper throughout their lifetime as a customer? */

SELECT COUNT(*)
FROM (SELECT a.name
      FROM orders o
      JOIN accounts a
      ON a.id = o.account_id
      GROUP BY 1
      HAVING SUM(o.total) > (
            SELECT t1.total
            FROM(SELECT a.name, SUM(o.standard_qty), SUM(o.total) total
            FROM accounts a
            JOIN orders o
            ON a.id = o.account_id
            GROUP BY 1
            ORDER BY 2 DESC
            LIMIT 1) t1
            )
      ) t2;

/* Question 4: For the customer that spent the most (in total over their lifetime as a customer) total_amt_usd, how many web_events did they have for each channel? */
SELECT a.name, w.channel, COUNT(*)
FROM accounts a
JOIN web_events w
ON a.id = w.account_id
GROUP BY 1, 2
HAVING a.name = (
      SELECT t1.name
      FROM (SELECT a.name, SUM(total_amt_usd) total_usd
            FROM accounts a
            JOIN orders o
            ON a.id = o.account_id
            GROUP BY 1
            ORDER BY 2 DESC
            LIMIT 1) t1
      );

/* Solution Provided
SELECT a.name, w.channel, COUNT(*)
FROM accounts a
JOIN web_events w
ON a.id = w.account_id AND a.id =  (SELECT id
                     FROM (SELECT a.id, a.name, SUM(o.total_amt_usd) tot_spent
                           FROM orders o
                           JOIN accounts a
                           ON a.id = o.account_id
                           GROUP BY a.id, a.name
                           ORDER BY 3 DESC
                           LIMIT 1) inner_table)
GROUP BY 1, 2
ORDER BY 3 DESC;
*/

/* Question 5: What is the lifetime average amount spent in terms of total_amt_usd for the top 10 total spending accounts? */
SELECT AVG(sum_total_usd) avg_tot_amt_usd
FROM (SELECT a.id, a.name, SUM(o.total_amt_usd) sum_total_usd
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY 1, 2
    ORDER BY 3 DESC
    LIMIT 10) t1;

/* Question 6: What is the lifetime average amount spent in terms of total_amt_usd, including only the companies that spent more per order, on average, than the average of all orders? */
/* Second Attempt - In line with solution provided. - Average amount per order by company average if the company was over the average of all orders = 4721.14 */
SELECT AVG(t1.cust_avg_amt)
FROM (SELECT o.account_id, AVG(total_amt_usd) cust_avg_amt
      FROM orders o
      GROUP BY 1
      HAVING AVG(o.total_amt_usd) > (
            SELECT AVG(o.total_amt_usd) avg_order_usd
            FROM orders o
            )
      ) t1;


/* Initial attempt - Average amount per order for companies whose average was over the average of all orders = 4434.22
SELECT AVG(total_amt_usd)
FROM orders o
WHERE o.account_id IN (
      SELECT o.account_id
      FROM orders o
      GROUP BY o.account_id
      HAVING AVG(o.total_amt_usd) > (
            SELECT AVG(o.total_amt_usd) avg_order_usd
            FROM orders o
            )
      );
*/

/* Your first WITH (CTE - Common Table Expression allows you to define a temporary result, such as a table, to then be referenced in a later part of the query.)
Question: Find the average number of events for each channel per day

Solution 1:
SELECT t1.channel, AVG(num_events_day) avg_num_events_day
FROM (SELECT DATE_TRUNC('day', w.occurred_at), w.channel, COUNT(*) num_events_day
      FROM web_events w
      GROUP BY 1, 2) t1
GROUP BY 1
ORDER BY 2 DESC;

WITH events AS (
    SELECT DATE_TRUNC('day', occurred_at),
           channel,
           COUNT(*) num_events_day
    FROM web_events
    GROUP BY 1, 2)
SELECT channel,
       AVG(num_events_day)
FROM evvents
GROUP BY 1
ORDER BY 2 DESC;
*/

/* General WITH queries - multiple tables
WITH table1 AS (
          SELECT *
          FROM web_events),

     table2 AS (
          SELECT *
          FROM accounts)


SELECT *
FROM table1
JOIN table2
ON table1.account_id = table2.id;
*/

/*********************************************
Quiz: Subquery - WITH Quiz
*********************************************/

/* Question 1: Provide the name of the sales_rep in each region with the largest amount of total_amt_usd sales. */
WITH tot_sales AS (
    SELECT s.name sales_rep,
           r.name region,
           SUM(o.total_amt_usd) total_usd
    FROM orders o
    JOIN accounts a
    ON o.account_id = a.id
    JOIN sales_reps s
    ON a.sales_rep_id = s.id
    JOIN region r
    ON s.region_id = r.id
    GROUP BY 1, 2),

  max_sales AS (
    SELECT t.region, MAX(t.total_usd) max_usd
    FROM tot_sales t
    GROUP BY 1)

SELECT t.region, t.sales_rep, t.total_usd
FROM tot_sales t
JOIN max_sales m
ON t.region = m.region AND t.total_usd = m.max_usd;

/* For the region with the largest sales total_amt_usd, how many total orders were placed? */
WITH region_sales AS (
    SELECT r.name region,
           SUM(o.total_amt_usd) total_amt
    FROM region r
    JOIN sales_reps s
    ON r.id = s.region_id
    JOIN accounts a
    ON s.id = a.sales_rep_id
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY 1),

  max_region_sales AS (
    SELECT MAX(r.total_amt) max_amt
    FROM region_sales r),

  max_region AS (
    SELECT r.region
    FROM region_sales r
    JOIN max_region_sales m
    ON r.total_amt = m.max_amt)

SELECT m.region,
       COUNT(*) tot_orders
FROM orders o
JOIN accounts a
ON a.id = o.account_id
JOIN sales_reps s
ON s.id = a.sales_rep_id
JOIN region r
ON r.id = s.region_id
JOIN max_region m
ON r.name = m.region
GROUP BY 1;

/* Solution provided
WITH t1 AS (
   SELECT r.name region_name, SUM(o.total_amt_usd) total_amt
   FROM sales_reps s
   JOIN accounts a
   ON a.sales_rep_id = s.id
   JOIN orders o
   ON o.account_id = a.id
   JOIN region r
   ON r.id = s.region_id
   GROUP BY r.name), 
t2 AS (
   SELECT MAX(total_amt)
   FROM t1)
SELECT r.name, COUNT(o.total) total_orders
FROM sales_reps s
JOIN accounts a
ON a.sales_rep_id = s.id
JOIN orders o
ON o.account_id = a.id
JOIN region r
ON r.id = s.region_id
GROUP BY r.name
HAVING SUM(o.total_amt_usd) = (SELECT * FROM t2);
*/

/* How many accounts had more total purchases than the account name which has bought the most standard_qty paper throughout their lifetime as a customer? */
WITH t1 AS (
    SELECT a.name,
           SUM(standard_qty) tot_std_qty,
           SUM(total) tot_qty
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 1),

  t2 AS (
    SELECT a.id
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY a.id
    HAVING SUM(o.total) > (SELECT tot_qty FROM t1))

SELECT COUNT(*)
FROM t2;

/* For the customer that spent the most (in total over their lifetime as a customer) total_amt_usd, how many web_events did they have for each channel? */
WITH t1 AS (
    SELECT a.id, a.name, SUM(o.total_amt_usd)
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY 1, 2
    ORDER BY 3 DESC
    LIMIT 1)

SELECT a.name, w.channel, COUNT(*)
FROM accounts a
JOIN web_events w
ON a.id = w.account_id AND a.id = (SELECT id FROM t1)
GROUP BY 1, 2;

/* What is the lifetime average amount spent in terms of total_amt_usd for the top 10 total spending accounts? */
WITH t1 AS (
    SELECT a.id, a.name, SUM(o.total_amt_usd) tot_amt
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY 1, 2
    ORDER BY 3 DESC
    LIMIT 10)

SELECT AVG(tot_amt)
FROM t1;

/* What is the lifetime average amount spent in terms of total_amt_usd, including only the companies that spent more per order, on average, than the average of all orders. */
WITH t1 AS (
    SELECT AVG(o.total_amt_usd)
    FROM orders o),

  t2 AS (
    SELECT a.name, AVG(o.total_amt_usd) avg_amt
    FROM accounts a
    JOIN orders o
    ON a.id = o.account_id
    GROUP BY 1
    HAVING AVG(o.total_amt_usd) > (SELECT * FROM t1))

SELECT AVG(avg_amt)
FROM t2;

/*
NESTED Query Example

SELECT *
FROM students
WHERE student_id
IN (SELECT DISTINCT student_id
    FROM gpa_table
    WHERE gpa>3.5
    );
*/

/*
INLINE Query Example

SELECT dept_name,
       max_gpa
FROM department_db x
     (SELECT dept_id
             MAX(gpa) as max_gpa
      FROM students
      GROUP BY dept_id
      )y
WHERE x.dept_id = y.dept_id
ORDER BY dept_name;
*/

/*
SCALAR Query Example

SELECT 
   (SELECT MAX(salary) FROM employees_db) AS top_salary,
   employee_name
FROM employees_db;
*/
