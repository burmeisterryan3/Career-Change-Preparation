/*
Advanced SQL

JOINS - 
INNER JOIN: produce results for which the join condition is matched in both tables (Venn Diagram center)
LEFT JOIN: also include unmatched rows from the left table, which is indicated in the “FROM” clause (Venn Diagram center and left circle)
RIGHT JOIN: include unmatched data from the right table -- the one that’s indicated in the JOIN clause (Venn Diagram center and right circle)
FULL OUTER JOIN: include unmatched rows from both tables being joined

LEFT JOIN - 
SELECT column_name(s)
FROM Table_A
LEFT JOIN Table_B ON Table_A.column_name = Table_B.column_name;

RIGHT JOIN - 
SELECT column_name(s)
FROM Table_A
RIGHT JOIN Table_B ON Table_A.column_name = Table_B.column_name

FULL OUTER JOIN - 
SELECT column_name(s)
FROM Table_A
FULL OUTER JOIN Table_B ON Table_A.column_name = Table_B.column_name;

FULL OUTER JOIN -
A full outer join returns unmatched records in each table with null values for the columns that came from the opposite table.
Use Case:
A common application of this is when joining two tables on a timestamp. Let’s say you’ve got one table containing the number of item 1 sold each day, and another containing the number of item 2 sold. If a certain date, like January 1, 2018, exists in the left table but not the right, while another date, like January 2, 2018, exists in the right table but not the left:
	- a left join would drop the row with January 2, 2018, from the result set
	- a right join would drop January 1, 2018, from the result set
The only way to make sure both January 1, 2018, and January 2, 2018, make it into the results is to do a full outer join

If you wanted to return unmatched rows only, which is useful for some cases of data assessment, you can isolate them by adding the following line to the end of the query:
WHERE Table_A.column_name IS NULL OR Table_B.column_name IS NULL
*/

/*********************************************
Quiz: FULL OUTER JOIN Quiz
*********************************************/

/* Question 1: Say you're an analyst at Parch & Posey and you want to see:
	- each account who has a sales rep and each sales rep that has an account (all of the columns in these returned rows will be full)
	- but also each account that does not have a sales rep and each sales rep that does not have an account (some of the columns in these returned rows will be empty)
Write a query with FULL OUTER JOIN to fit the above described Parch & Posey scenario (selecting all of the columns in both of the relevant tables, accounts and sales_reps) */
SELECT s.name sales_rep, a.name account
FROM accounts a
FULL OUTER JOIN sales_reps s
ON s.id = a.sales_rep_id
/* Use below line to display unmatched rows. NOTE: There are no unmatched rows for this query. */
/* WHERE s.id IS NULL OR a.sales_rep_id IS NULL; */

/*
EXAMPLE

SELECT orders.id,
       orders.occurred_at  AS order_date,
       events.*
FROM orders
LEFT JOIN web_events events
      ON events.account_id = orders.account_id
      AND events.occurred_at < orders.occurred_at
WHERE  DATE_TRUNC('month', orders.occurred_at) =
        (SELECT DATE_TRUNC('month', MIN(orders.occurred_at)) FROM orders)
ORDER BY orders.account_id, orders.occurred_at, events.occurred_at
*/

/*********************************************
Quiz: JOINS with Comparison Operators Quiz
*********************************************/

/* Question 1: Write a query that left joins the accounts table and the sales_reps tables on each sale rep's ID number and joins it using the < comparison operator on accounts.primary_poc and sales_reps.name, like so: accounts.primary_poc < sales_reps.name. The query results should be a table with three columns: the account name (e.g. Johnson Controls), the primary contact name (e.g. Cammy Sosnowski), and the sales representative's name (e.g. Samuel Racine). */

SELECT a.name account,
       a.primary_poc,
       s.name sales_rep
FROM accounts a
LEFT JOIN sales_reps s
ON s.id = a.sales_rep_id AND
   a.primary_poc < s.name;

/*
Self JOIN
One of the most common use cases for self JOINs is in cases where two events occurred, one after another. Using inequalities in conjunction with self JOINs is common.

What use case below is appropriate for self joins?
    When you want to calculate the running total of orders made over the course of a year (Window Function)
    When you want to show both parent and child relationships within a family tree  (YES)
    When you want the first four digits of a student ID as a unique identifier (LEFT/SUBSTR)
    When you want to join all records of two tables to determine where employees live (JOIN)
*/

/*********************************************
Quiz: Self JOINs Quiz
*********************************************/

/* Question 1: Modify the query from the previous video, which is pre-populated in the SQL Explorer below, to perform the same interval analysis except for the web_events table. Also:
    - change the interval to 1 day to find those web events that occurred after, but not more than 1 day after, another web event
    - add a column for the channel variable in both instances of the table in your query

SELECT o1.id AS o1_id,
       o1.account_id AS o1_account_id,
       o1.occurred_at AS o1_occurred_at,
       o2.id AS o2_id,
       o2.account_id AS o2_account_id,
       o2.occurred_at AS o2_occurred_at
  FROM orders o1
 LEFT JOIN orders o2
   ON o1.account_id = o2.account_id
  AND o2.occurred_at > o1.occurred_at
  AND o2.occurred_at <= o1.occurred_at + INTERVAL '28 days'
ORDER BY o1.account_id, o1.occurred_at
*/

SELECT w1.id AS w1_id,
       w1.account_id AS w1_account_id,
       w1.occurred_at AS w1_occurred_at,
       w1.channel AS w1_channel,
       w2.id AS w2_id,
       w2.account_id AS w2_account_id,
       w2.occurred_at AS w2_occurred_at,
       w2.channel AS w2_channel
FROM web_events w1
LEFT JOIN web_events w2
ON w1.account_id = w2.account_id
   AND w2.occurred_at > w1.occurred_at
   AND w2.occurred_at <= w1.occurred_at + INTERVAL '1 day'
ORDER BY w1.account_id, w1.occurred_at, w1.channel

/*
UNION
https://www.techonthenet.com/sql/union.php

Typically, the use case for leveraging the UNION command in SQL is when a user wants to pull together distinct values of specified columns that are spread across multiple tables.

SQL's two strict rules for appending data:
    - Both tables must have the same number of columns.
    - Those columns must have the same data types in the same order as the first table

A common misconception is that column names have to be the same. Column names, in fact, don't need to be the same to append two tables but you will find that they typically are (e.g. dataset that is split across multiple tables).

UNION removes duplicate rows.
UNION ALL does not remove duplicate rows.

SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions]
UNION
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions];
*/

/*
UNION ALL Example:

CREATE VIEW web_events_2
AS (SELECT * FROM web_events)

SELECT *
FROM web_events
WHERE channel = 'facebook'
UNION ALL
SELECT *
FROM web_events_2
*/

/*
UNION Example:

CREATE VIEW web_events_2
AS (SELECT * FROM web_events)

WITH web_events AS (
      SELECT *
      FROM web_events
      UNION ALL
      SELECT *
      FROM web_events_2
     )
SELECT channel,
       COUNT(*) AS sessions
FROM  web_events
GROUP BY 1
ORDER BY 2 DESC
*/

/*
UNION Question: What use case below is it appropriate to use a union?
ANSWER: When you want to determine all reasons students are late. Currently, each late reason is maintained within tables corresponding to the grade the student is in.
*/

/*********************************************
Quiz: Self JOINs Quiz
*********************************************/

/* Question 1: Write a query that uses UNION ALL on two instances (and selecting all columns) of the accounts table. Then inspect the results and answer the subsequent quiz. */
SELECT *
FROM accounts
UNION ALL
SELECT *
FROM accounts;

/* Question 2: Add a WHERE clause to each of the tables that you unioned in the query above, filtering the first table where name equals Walmart and filtering the second table where name equals Disney. Inspect the results then answer the subsequent quiz. */
SELECT *
FROM accounts a1
WHERE a1.name = 'Walmart'
UNION ALL
SELECT *
FROM accounts a2
WHERE a2.name = 'Disney';

/* Question 3: How else could the above query have been written? */
SELECT *
FROM accounts
WHERE name = 'Walmart' OR name = 'Disney';

/* Question 4: Perform the union in Question 1 in a common table expression and name it double_accounts. Then do a COUNT the number of times a name appears in the double_accounts table. If you do this correctly, your query results should have a count of 2 for each name. *//

WITH double_accounts AS (
    SELECT *
    FROM accounts
    UNION ALL
    SELECT *
    FROM accounts)

SELECT name, COUNT(*)
FROM double_accounts
GROUP BY 1
ORDER BY 2 DESC;

/*
Performance Tuning 1 - Reducing the number of calculations

One way to make a query run faster is to reduce the number of calculations that need to be performed. Some of the high-level things that will affect the number of calculations a given query will make include:
    - Table size
    - Joins
    - Aggregations

Query runtime is also dependent on some things that you can’t really control related to the database itself:
    - Other users running queries concurrently on the database
    - Database software and optimization (e.g., Postgres is optimized differently than Redshift)

Question: Select all of the following statements that are ture about tuning performance with LIMIT.
ANSWERS:
    - If you have time series data, limiting to a small time window can make your queries run more quickly.
    - Testing your queries on a subset of data, finalizing your query, then removing the subset limitation is a sound strategy.
    - When working with subquereis, limiting the amount of data you're working with in the place where it will be exeucted will have the maximum impact on query run time.

SELECT account_id,
       SUM(poster_qty) AS sum_poster_qty
FROM   (SELECT * FROM orders LIMIT 100) sub
WHERE  occurred_at >= '2016-01-01'
AND    occurred_at < '2016-07-01'
GROUP BY 1;
*/

/*
Performance Tuning 2 - Makeing JOINs less complicated

The second thing you can do is to make joins less complicated, that is, reduce the number of rows that need to be evaluated. It is better to reduce table sizes before joining them. This can be done by creating subqueries and joining them to an outer query. Aggregating before joining will improve query speed; however, be sure that what you are doing is logically consistent. Accuracy is more important than run speed.

Aggregation following JOIN = SLOW over large tables
SELECT accounts.name,
       COUNT(*) AS web_events
FROM accounts
JOIN web_events events
ON events.account_id = accounts.id
GROUP BY 1
ORDER BY 2;

Aggregation before JOIN = FASTER over large tables
SELECT a.name,
       sub.web_events
FROM   (SELECT account_id,
               COUNT(*) AS web_events
        FROM web_events
        GROUP BY 1) sub
JOIN   accounts a
ON     a.id = sub.account_id
ORDER BY 2 DESC;
*/

/*
Performance Tuning 3 - EXPLAIN

Adding the command EXPLAIN at the beginning of any query allows you to get a sense of how long it will take your query to run. This will output a Query Plan which outlines the execution order of the query. The query plan will attach a cost to the query and the higher the cost, the longer the runtime. EXPLAIN is most useful to identify and modify those steps that are expensive. Do this then run EXPLAIN again to see if the speed/cost has improved.
*/

/*
Performance Tuning 3 - JOINing Subqueries

SLOW Query - JOINs and then aggregates ~79k rows
SELECT DATE_TRUNC('day', o.occurred_at) AS date,
       COUNT(DISTINCT a.sales_rep_id) AS active_sales_reps,
       COUNT(DISTINCT o.id) AS orders,
       COUNT(DISTInct we.id) AS web_visits
FROM   accounts a
JOIN   orders o
ON     o.account_id = a.id
JOIN   web_events we
ON     DATE_TRUNC('day', we.occurred_at) = DATE_TRUNC('day', o.occurred_at)
GROUP BY 1
ORDER BY 1 DESC

FASTER Query - Aggregates and then JOINs 2 tables of approx. 1k rows
SELECT COALESCE(orders.date, web_events.date) AS date,
       orders.active_sales_reps,
       orders.orders,
       web_events.web_visits
FROM(  
   SELECT DATE_TRUNC('day', o.occurred_at) AS date,
          COUNT(DISTINCT a.sales_rep_id) AS active_sales_reps,
          COUNT(DISTINCT o.id) AS orders
   FROM   accounts a
   JOIN   orders o
   ON     o.account_id = a.id
   GROUP BY 1) AS orders

FULL JOIN(
   SELECT DATE_TRUNC('day', we.occurred_at) AS date,
          COUNT(we.id) AS web_visits
   FROM   web_events we
   GROUP BY 1) AS web_events

ON orders.date = web_events.date
ORDER BY 1 DESC
*/