/*
SELECT *
FROM web_events
JOIN accounts
ON web_events.account_id = accounts.id
JOIN orders
ON accounts.id = orders.account_id
*/

/*********************************************
Quiz:  JOIN
*********************************************/

/* Question 1: Try pulling all the data from the accounts table, and all the data from the orders table.*/
SELECT orders.*,
       accounts.*
FROM orders
JOIN accounts
ON orders.account_id = accounts.id;

/* Question 2: Try pulling standard_qty, gloss_qty, and poster_qty from the orders table, and the website and the primary_poc from the accounts table.*/
SELECT orders.standard_qty,
       orders.gloss_qty,
       orders.poster_qty,
       accounts.website,
       accounts.primary_poc
FROM orders
JOIN accounts
ON orders.account_id = accounts.id;


/*********************************************
Quiz:  JOIN Questions Part 1
*********************************************/

/* Question 1: Provide a table for all web_events associated with the account name of Walmart. There should be three columns. Be sure to include the primary_poc, time of the event, and the channel for each event. Additionally, you might choose to add a fourth column to assure only Walmart events were chosen.*/
SELECT a.primary_poc, w.occurred_at, w.channel, a.name
FROM accounts a
JOIN web_events w
ON a.id = w.account_id
WHERE a.name = 'Walmart';

/* Question 2: Provide a table that provides the region for each sales_rep along with their associated accounts. Your final table should include three columns: the region name, the sales rep name, and the account name. Sort the accounts alphabetically (A-Z) according to the account name.*/
SELECT a.name account, r.id region, s.name rep
FROM region r
JOIN sales_reps s
ON r.id = s.region_id
JOIN accounts a
ON s.id = a.sales_rep_id
ORDER BY a.name;

/* Question 3: Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) for the order. Your final table should have 3 columns: region name, account name, and unit price. A few accounts have 0 for total, so I divided by (total + 0.01) to assure not dividing by zero.*/
SELECT r.name region, a.name account, o.total_amt_usd/(o.total + 0.01) unit_price
FROM region r
JOIN sales_reps s
ON r.id = s.region_id
JOIN accounts a
ON s.id = a.sales_rep_id
JOIN orders o
ON a.id = o.account_id;

/*
LEFT JOIN with WHERE - JOIN occurs before WHERE filters the result
*/

SELECT o.*, a.*
FROM orders o
LEFT JOIN accounts a
ON o.account_id = a.id
WHERE a.sales_rep_id = 321500;

/*
LEFT JOIN with AND - JOIN occurs after AND filers the data to query
*/

SELECT o.*, a.*
FROM orders o
LEFT JOIN accounts a
ON o.account_id = a.id
AND a.sales_rep_id = 321500;

/*********************************************
Quiz:  JOIN Questions Part 1
*********************************************/

/* Question 1: Provide a table that provides the region for each sales_rep along with their associated accounts. This time only for the Midwest region. Your final table should include three columns: the region name, the sales rep name, and the account name. Sort the accounts alphabetically (A-Z) according to the account name. */
SELECT a.name account_name, s.name rep_name, r.name region_name
FROM sales_reps s
JOIN region r
ON r.id = s.region_id AND r.name = 'Midwest'
JOIN accounts a
ON s.id = a.sales_rep_id
ORDER BY a.name;

/* Question 2: Provide a table that provides the region for each sales_rep along with their associated accounts. This time only for accounts where the sales rep has a first name starting with S and in the Midwest region. Your final table should include three columns: the region name, the sales rep name, and the account name. Sort the accounts alphabetically (A-Z) according to the account name. */
SELECT a.name account_name, s.name rep_name, r.name region_name
FROM sales_reps s
JOIN region r
ON r.id = s.region_id AND r.name = 'Midwest'
JOIN accounts a
ON s.id = a.sales_rep_id
WHERE s.name LIKE 'S%'
ORDER BY a.name;

/* Question 3: Provide a table that provides the region for each sales_rep along with their associated accounts. This time only for accounts where the sales rep has a last name starting with K and in the Midwest region. Your final table should include three columns: the region name, the sales rep name, and the account name. Sort the accounts alphabetically (A-Z) according to the account name. */
SELECT a.name account_name, s.name rep_name, r.name region_name
FROM sales_reps s
JOIN region r
ON r.id = s.region_id AND r.name = 'Midwest'
JOIN accounts a
ON s.id = a.sales_rep_id
WHERE s.name LIKE '% K%'
ORDER BY a.name;

/* Question 4: Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) for the order. However, you should only provide the results if the standard order quantity exceeds 100. Your final table should have 3 columns: region name, account name, and unit price. In order to avoid a division by zero error, adding .01 to the denominator here is helpful total_amt_usd/(total+0.01). */
SELECT a.name account_name, o.total_amt_usd/(total+0.01) unit_price, r.name region_name
FROM orders o
JOIN accounts a
ON a.id = o.account_id AND o.standard_qty > 100
JOIN sales_reps s
ON a.sales_rep_id = s.id
JOIN region r
ON s.region_id = r.id;

/* Question 5: Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) for the order. However, you should only provide the results if the standard order quantity exceeds 100 and the poster order quantity exceeds 50. Your final table should have 3 columns: region name, account name, and unit price. Sort for the smallest unit price first. In order to avoid a division by zero error, adding .01 to the denominator here is helpful (total_amt_usd/(total+0.01).*/
SELECT a.name account_name, o.total_amt_usd/(total+0.01) unit_price, r.name region_name
FROM orders o
JOIN accounts a
ON a.id = o.account_id AND o.standard_qty > 100 AND o.poster_qty > 50
JOIN sales_reps s
ON a.sales_rep_id = s.id
JOIN region r
ON s.region_id = r.id
ORDER BY unit_price;

/* Question 6: Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) for the order. However, you should only provide the results if the standard order quantity exceeds 100 and the poster order quantity exceeds 50. Your final table should have 3 columns: region name, account name, and unit price. Sort for the largest unit price first. In order to avoid a division by zero error, adding .01 to the denominator here is helpful (total_amt_usd/(total+0.01). */
SELECT a.name account_name, o.total_amt_usd/(total+0.01) unit_price, r.name region_name
FROM orders o
JOIN accounts a
ON a.id = o.account_id AND o.standard_qty > 100 AND o.poster_qty > 50
JOIN sales_reps s
ON a.sales_rep_id = s.id
JOIN region r
ON s.region_id = r.id
ORDER BY unit_price DESC;

/* Question 7: What are the different channels used by account id 1001? Your final table should have only 2 columns: account name and the different channels. You can try SELECT DISTINCT to narrow down the results to only the unique values. */
SELECT DISTINCT a.name, w.channel
FROM accounts a
JOIN web_events w
ON a.id = w.account_id AND a.id = 1001;

/* Question 8: Find all the orders that occurred in 2015. Your final table should have 4 columns: occurred_at, account name, order total, and order total_amt_usd. */
SELECT o.occurred_at, a.name, o.total, o.total_amt_usd
FROM orders o
LEFT JOIN accounts a
ON a.id = o.account_id
WHERE o.occurred_at BETWEEN '2015-01-01' AND '2016-01-01'
ORDER BY o.occurred_at;
