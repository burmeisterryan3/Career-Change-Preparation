/*********************************************
Quiz:  SUM
*********************************************/

/* Question 1: Find the total amount of poster_qty paper ordered in the orders table. */
SELECT SUM(poster_qty) AS total_poster
FROM orders;

/* Question 2: Find the total amount of standard_qty paper ordered in the orders table. */
SELECT SUM(standard_qty) AS total_standard
FROM orders;

/* Question 3: Find the total dollar amount of sales using the total_amt_usd in the orders table. */
SELECT SUM(total_amt_usd) AS total_sales
FROM orders;

/* Question 4: Find the total amount spent on standard_amt_usd and gloss_amt_usd paper for each order in the orders table. This should give a dollar amount for each order in the table. */
SELECT standard_amt_usd + gloss_amt_usd AS total_standard_gloss
FROM orders;

/* Question 5: Find the standard_amt_usd per unit of standard_qty paper. Your solution should use both aggregation and a mathematical operator. */
SELECT SUM(standard_amt_usd)/SUM(standard_qty) AS standard_unit_price
FROM orders;

/*********************************************
Quiz:  MIN, MAX, & AVERAGE
*********************************************/

/* Question 1: When was the earliest order ever placed? You only need to return the date. */
SELECT MIN(occurred_at) as earliest_order
FROM orders;

/* Question 2: Try performing the same query as in question 1 without using an aggregation function. */
SELECT occurred_at as earliest_order
FROM orders
ORDER BY occurred_at
LIMIT 1;

/* Question 3: When did the most recent (latest) web_event occur? */
SELECT MAX(occurred_at) AS latest_event
FROM web_events;

/* Question 4: Try to perform the result of the previous query without using an aggregation function. */
SELECT occurred_at AS latest_event
FROM web_events
ORDER BY occurred_at DESC
LIMIT 1;

/* Question 5: Find the mean (AVERAGE) amount spent per order on each paper type, as well as the mean amount of each paper type purchased per order. Your final answer should have 6 values - one for each paper type for the average number of sales, as well as the average amount. */
SELECT AVG(o.standard_amt_usd) AS avg_standard_price,
       AVG(o.poster_amt_usd) AS avg_poster_price,
       AVG(o.gloss_amt_usd) AS avg_gloss_price,
       AVG(o.standard_qty) AS avg_standard_qty,
       AVG(o.poster_qty) AS avg_poster_qty,
       AVG(o.gloss_qty) AS avg_gloss_qty
FROM orders o;

/* Question 6: Via the video, you might be interested in how to calculate the MEDIAN. Though this is more advanced than what we have covered so far try finding - what is the MEDIAN total_usd spent on all orders?

SELECT *
FROM (SELECT total_amt_usd
   FROM orders
   ORDER BY total_amt_usd
   LIMIT 3457) AS Table1
ORDER BY total_amt_usd DESC
LIMIT 2;

Since there are 6912 orders - we want the average of the 3457 and 3456 order amounts when ordered. This is the average of 2483.16 and 2482.55. This gives the median of 2482.855. This obviously isn't an ideal way to compute. If we obtain new orders, we would have to change the limit. SQL didn't even calculate the median for us. The above used a SUBQUERY, but you could use any method to find the two necessary values, and then you just need the average of them.*/


/*********************************************
Quiz:  GROUP BY
*********************************************/

/* Question 1: Which account (by name) placed the earliest order? Your solution should have the account name and the date of the order. */
SELECT a.name,
       o.occurred_at
FROM accounts a
JOIN orders o
ON a.id = o.account_id
ORDER BY occurred_at
LIMIT 1;

/* Question 2: Find the total sales in usd for each account. You should include two columns - the total sales for each company's orders in usd and the company name. */
SELECT a.name,
       SUM(total_amt_usd) AS total_sales_usd
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY a.name
ORDER BY a.name;

/* Question 3: Via what channel did the most recent (latest) web_event occur, which account was associated with this web_event? Your query should return only three values - the date, channel, and account name. */
SELECT a.name account_name,
       w.occurred_at,
       w.channel
FROM accounts a
JOIN web_events w
ON a.id = w.account_id
ORDER BY w.occurred_at DESC
LIMIT 1;

/* Question 4: Find the total number of times each type of channel from the web_events was used. Your final table should have two columns - the channel and the number of times the channel was used. */
SELECT w.channel,
       COUNT(w.channel) AS channel_occurrence /* or - COUNT(*) */
FROM web_events w
GROUP BY w.channel
ORDER BY w.channel;

/* Question 5: Who was the primary contact associated with the earliest web_event? */
SELECT a.primary_poc AS earliest_web_event_poc
FROM accounts a
JOIN web_events w
ON a.id = w.account_id
ORDER BY w.occurred_at
LIMIT 1;

/* Question 6: What was the smallest order placed by each account in terms of total usd. Provide only two columns - the account name and the total usd. Order from smallest dollar amounts to largest. */
SELECT a.name account_name,
       MIN(o.total_amt_usd) AS min_order_placed
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY a.name
ORDER BY min_order_placed;

/* Question 7: Find the number of sales reps in each region. Your final table should have two columns - the region and the number of sales_reps. Order from the fewest reps to most reps. */
SELECT r.name region,
       COUNT(s.id) AS num_sales_reps
FROM region r
JOIN sales_reps s
ON r.id = s.region_id
GROUP BY region
ORDER BY num_sales_reps;

/*********************************************
Quiz:  GROUP BY Part II
*********************************************/

/* Question 1: For each account, determine the average amount of each type of paper they purchased across their orders. Your result should have four columns - one for the account name and one for the average quantity purchased for each of the paper types for each account. */
SELECT a.name,
       AVG(o.standard_qty) AS avg_standard_qty,
       AVG(o.poster_qty) AS avg_poster_qty,
       AVG(o.gloss_qty) AS avg_glossy_qty
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY a.name
ORDER BY a.name;

/* Question 2: For each account, determine the average amount spent per order on each paper type. Your result should have four columns - one for the account name and one for the average amount spent on each paper type. */
SELECT a.name,
       AVG(o.standard_amt_usd) AS avg_standard_amt,
       AVG(o.poster_amt_usd) AS avg_poster_amt,
       AVG(o.gloss_amt_usd) AS avg_glossy_amt
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY a.name
ORDER BY a.name;

/* Question 3: Determine the number of times a particular channel was used in the web_events table for each sales rep. Your final table should have three columns - the name of the sales rep, the channel, and the number of occurrences. Order your table with the highest number of occurrences first. */
SELECT s.name,
       w.channel,
       COUNT(w.channel) AS num_occurrences /* or - COUNT(*) num_events */
FROM sales_reps s
JOIN accounts a
ON s.id = a.sales_rep_id
JOIN web_events w
ON a.id = w.account_id
GROUP BY s.name, w.channel
ORDER BY num_occurrences DESC; /* or - ORDER BY num_events DESC */

/* Question 4: Determine the number of times a particular channel was used in the web_events table for each region. Your final table should have three columns - the region name, the channel, and the number of occurrences. Order your table with the highest number of occurrences first. */
SELECT r.name region,
       w.channel,
       COUNT(w.channel) as num_occurrences /* or - COUNT(*) num_events */
FROM region r
JOIN sales_reps s
ON r.id = s.region_id
JOIN accounts a
ON s.id = a.sales_rep_id
JOIN web_events w
ON a.id = w.account_id
GROUP BY region, w.channel
ORDER BY num_occurrences DESC; /* or - ORDER BY num_events DESC */

/*********************************************
Quiz:  DISTINCT
*********************************************/

/* Question 1: Use DISTINCT to test if there are any accounts associated with more than one region. */
/* Remove DISTINCT to show that the solution has the same number of rows */
SELECT DISTINCT a.id,
       r.name
FROM accounts a
JOIN sales_reps s
ON s.id = a.sales_rep_id
JOIN region r
ON r.id = s.region_id
ORDER BY a.id;

/* Question 2: Have any sales reps worked on more than one account? */
/* Remove DISTINCT to show that the solution has the same number of rows */
SELECT DISTINCT s.name sales_rep,
       a.name account
FROM accounts a
JOIN sales_reps s
ON s.id = a.sales_rep_id
ORDER BY sales_rep;


/*********************************************
Quiz:  HAVING
*********************************************/

/* Question 1: How many of the sales reps have more than 5 accounts that they manage? */
SELECT s.name sales_rep,
       COUNT(*) AS num_accounts
FROM accounts a
JOIN sales_reps s
ON s.id = a.sales_rep_id
GROUP BY sales_rep
HAVING COUNT(*) > 5
ORDER BY sales_rep;

/*
Subquery solution for Question 1.

SELECT COUNT(*) num_reps_above5
FROM(SELECT s.id, s.name, COUNT(*) num_accounts
     FROM accounts a
     JOIN sales_reps s
     ON s.id = a.sales_rep_id
     GROUP BY s.id, s.name
     HAVING COUNT(*) > 5
     ORDER BY num_accounts) AS Table1;
*/

/* Question 2: How many accounts have more than 20 orders? */
SELECT a.name,
       COUNT(*) num_orders
FROM orders o
JOIN accounts a
ON o.account_id = a.id
GROUP BY a.name
HAVING COUNT(*) > 20
ORDER BY num_orders;

/* Question 3: Which account has the most orders? */
SELECT a.name,
       COUNT(*) num_orders
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY a.name
ORDER BY num_orders DESC
LIMIT 1;

/* Question 4: Which accounts spent more than 30,000 usd total across all orders? */
SELECT a.name,
       SUM(o.total_amt_usd) total_usd
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY a.name
HAVING SUM(o.total_amt_usd) > 30000
ORDER BY total_usd;

/* Question 5: Which accounts spent less than 1,000 usd total across all orders? */
SELECT a.name,
       SUM(o.total_amt_usd) total_usd
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY a.name
HAVING SUM(o.total_amt_usd) < 1000
ORDER BY total_usd;

/* Question 6: Which account has spent the most with us? */
SELECT a.name,
       SUM(o.total_amt_usd) total_usd
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY a.name
ORDER BY total_usd DESC
LIMIT 1;

/* Question 7: Which account has spent the least with us? */
SELECT a.name,
       SUM(o.total_amt_usd) total_usd
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY a.name
ORDER BY total_usd
LIMIT 1;

/* Question 8: Which accounts used facebook as a channel to contact customers more than 6 times? */
SELECT a.name,
       w.channel,
       COUNT(*) num_contacts
FROM accounts a
JOIN web_events w
ON a.id = w.account_id
GROUP BY a.name, w.channel
HAVING w.channel = 'facebook' AND COUNT(*) > 6
ORDER BY a.name;

/* Question 9: Which account used facebook most as a channel? */
SELECT a.name,
       COUNT(*) num_contacts
FROM accounts a
JOIN web_events w
ON a.id = w.account_id AND w.channel = 'facebook'
GROUP BY a.name
ORDER BY num_contacts DESC
LIMIT 1;

/* Question 10: Which channel was most frequently used by most accounts? */
SELECT a.name,
       w.channel,
       COUNT(*) num_channel
FROM accounts a
JOIN web_events w
ON a.id = w.account_id
GROUP BY a.name, w.channel
ORDER BY num_channel DESC
LIMIT 10;

/*********************************************
Quiz: DATE Functions
*********************************************/

/* Question 1: Find the sales in terms of total dollars for all orders in each year, ordered from greatest to least. Do you notice any trends in the yearly sales totals? */
SELECT DATE_PART('year', occurred_at) AS ord_year,
       SUM(total_amt_usd) AS year_totals
FROM orders
GROUP BY 1
ORDER BY 1 DESC;

/*
Removing 2013 and 2017... only one month of data for 2013 and 2017 each. Should do this for the rest of the orders as well.

SELECT DATE_PART('month', occurred_at) ord_month, SUM(total_amt_usd) total_spent
FROM orders
WHERE occurred_at BETWEEN '2014-01-01' AND '2017-01-01'
GROUP BY 1
ORDER BY 2 DESC;
*/


/* Question 2: Which month did Parch & Posey have the greatest sales in terms of total dollars? Are all months evenly represented by the dataset? */
SELECT DATE_PART('month', occurred_at) AS ord_month,
       SUM(total_amt_usd) AS month_totals
FROM orders
GROUP BY 1
ORDER BY 2 DESC;

/* Question 3: Which year did Parch & Posey have the greatest sales in terms of the total number of orders? Are all years evenly represented by the dataset? */
SELECT DATE_PART('year', occurred_at) AS ord_year,
       COUNT(id) AS yearly_order_totals
FROM orders
GROUP BY 1
ORDER BY 2 DESC;

/* Question 4: Which month did Parch & Posey have the greatest sales in terms of the total number of orders? Are all months evenly represented by the dataset? */
SELECT DATE_PART('month', occurred_at) AS ord_month,
       COUNT(id) AS monthly_order_totals
FROM orders
GROUP BY 1
ORDER BY 2 DESC;

/* Question 5: In which month of which year did Walmart spend the most on gloss paper in terms of dollars? */
SELECT DATE_PART('year', o.occurred_at) AS ord_year,
       DATE_PART('month', o.occurred_at) AS ord_month,
       SUM(o.gloss_amt_usd) AS monthly_gloss_totals
FROM orders o
JOIN accounts a
ON a.id = o.account_id
WHERE a.name = 'Walmart'
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 1;

/*
Or using DATE_TRUNC...

SELECT DATE_TRUNC('month', o.occurred_at) AS ord_month,
       SUM(o.gloss_amt_usd) AS monthly_gloss_totals
FROM orders o
JOIN accounts a
ON a.id = o.account_id
WHERE a.name = 'Walmart'
GROUP BY 1
ORDER BY 2 
LIMIT 1;
*/

/*********************************************
Quiz: CASE
*********************************************/

/* Examples

#1
SELECT account_id, CASE WHEN standard_qty = 0 OR standard_qty IS NULL THEN 0
                        ELSE standard_amt_usd/standard_qty END AS unit_price
FROM orders
LIMIT 10;

#2
SELECT CASE WHEN total > 500 THEN 'OVer 500'
            ELSE '500 or under' END AS total_group,
            COUNT(*) AS order_count
FROM orders
GROUP BY 1;

#3
SELECT account_id,
       occurred_at,
       total,
       CASE WHEN total > 500 THEN 'Over 500'
            WHEN total > 300 AND total <= 500 THEN '301 - 500'
            WHEN total > 100 AND total <=300 THEN '101 - 300'
            ELSE '100 or under' END AS total_group
FROM orders;
*/

/* Question 1: Write a query to display for each order, the account ID, the total amount of the order, and the level of the order - ‘Large’ or ’Small’ - depending on if the order is $3000 or more, or smaller than $3000. */
SELECT a.id,
       o.total_amt_usd,
       CASE WHEN total_amt_usd >= 3000 THEN 'Large'
            ELSE 'Small' END AS ord_level
FROM accounts a
JOIN orders o
ON a.id = o.account_id;

/* Question 2: Write a query to display the number of orders in each of three categories, based on the total number of items in each order. The three categories are: 'At Least 2000', 'Between 1000 and 2000' and 'Less than 1000'. */
SELECT CASE WHEN o.total_amt_usd >= 2000 THEN 'At Least 2000'
            WHEN o.total_amt_usd >= 1000 AND o.total_amt_usd < 2000 THEN 'Between 1000 and 2000'
            ELSE 'Less than 1000' END AS category,
       COUNT(*) AS num_items
FROM orders o
GROUP BY 1;

/* Question 3: We would like to understand 3 different levels of customers based on the amount associated with their purchases. The top-level includes anyone with a Lifetime Value (total sales of all orders) greater than 200,000 usd. The second level is between 200,000 and 100,000 usd. The lowest level is anyone under 100,000 usd. Provide a table that includes the level associated with each account. You should provide the account name, the total sales of all orders for the customer, and the level. Order with the top spending customers listed first. */
SELECT a.name,
       SUM(o.total_amt_usd) total_usd,
       CASE WHEN SUM(o.total_amt_usd) > 200000 THEN 'Top-Level'
            WHEN SUM(o.total_amt_usd) > 100000 AND SUM(o.total_amt_usd) <= 200000 THEN 'Mid-Level'
            ELSE 'Low-Level' END AS lifetime_value
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY a.name
ORDER BY 2 DESC;

/* Question 4: We would now like to perform a similar calculation to the first, but we want to obtain the total amount spent by customers only in 2016 and 2017. Keep the same levels as in the previous question. Order with the top spending customers listed first. */
SELECT a.name,
       DATE_PART('year', o.occurred_at) AS ord_year,
       SUM(o.total_amt_usd) total_usd,
       CASE WHEN SUM(o.total_amt_usd) > 200000 THEN 'Top-Level'
            WHEN SUM(o.total_amt_usd) > 100000 AND SUM(o.total_amt_usd) <= 200000 THEN 'Mid-Level'
            ELSE 'Low-Level' END AS lifetime_value
FROM accounts a
JOIN orders o
ON a.id = o.account_id
WHERE o.occurred_at BETWEEN '2016-01-01' AND '2018-01-01'
GROUP BY a.name, ord_year
ORDER BY total_usd DESC;

/*
Solution provided: 
SELECT a.name, SUM(total_amt_usd) total_spent, 
  CASE WHEN SUM(total_amt_usd) > 200000 THEN 'top'
  WHEN  SUM(total_amt_usd) > 100000 THEN 'middle'
  ELSE 'low' END AS customer_level
FROM orders o
JOIN accounts a
ON o.account_id = a.id
WHERE occurred_at > '2015-12-31' 
GROUP BY 1
ORDER BY 2 DESC;
*/

/* Question 5: We would like to identify top-performing sales reps, which are sales reps associated with more than 200 orders. Create a table with the sales rep name, the total number of orders, and a column with top or not depending on if they have more than 200 orders. Place the top salespeople first in your final table.*/
SELECT s.name,
       COUNT(*) AS num_orders,
       CASE WHEN COUNT(*) > 200 THEN 'yes'
            ELSE 'no' END AS top_rep
FROM orders o
JOIN accounts a
ON o.account_id = a.id
JOIN sales_reps s
ON a.sales_rep_id = s.id
GROUP BY s.name
ORDER BY 2 DESC;

/* Question 6: The previous didn't account for the middle, nor the dollar amount associated with the sales. Management decides they want to see these characteristics represented as well. We would like to identify top-performing sales reps, which are sales reps associated with more than 200 orders or more than 750000 in total sales. The middle group has any rep with more than 150 orders or 500000 in sales. Create a table with the sales rep name, the total number of orders, total sales across all orders, and a column with top, middle, or low depending on these criteria. Place the top salespeople based on the dollar amount of sales first in your final table. You might see a few upset salespeople by this criteria! */
SELECT s.name,
       COUNT(*) AS num_orders,
       SUM(o.total_amt_usd) AS total_sales_usd,
       CASE WHEN COUNT(*) > 200 OR SUM(o.total_amt_usd) > 750000 THEN 'top'
            WHEN COUNT(*) > 150 OR SUM(o.total_amt_usd) > 500000 THEN 'middle'
            ELSE 'low' END AS sales_rep_performance
FROM orders o
JOIN accounts a
ON o.account_id = a.id
JOIN sales_reps s
ON a.sales_rep_id = s.id
GROUP BY s.name
ORDER BY 3 DESC;