/*********************************************
Quiz: Practce Quiz #1
*********************************************/

/* Question 1: Let's start with creating a table that provides the following details: actor's first and last name combined as full_name, film title, film description and length of the movie. How many rows are there in the table? */

SELECT CONCAT(first_name, ' ', last_name) full_name,
	   f.title film_title,
	   f.description,
	   f.length
FROM actor a
JOIN film_actor fa
ON a.actor_id = fa.actor_id
JOIN film f
ON f.film_id = fa.film_id;

/* Question 2: Write a query that creates a list of actors and movies where the movie length was more than 60 minutes. How many rows are there in this query result? */

SELECT CONCAT(first_name, ' ', last_name) full_name, f.title film_title
FROM actor a
JOIN film_actor fa
ON a.actor_id = fa.actor_id
JOIN film f
ON f.film_id = fa.film_id
WHERE f.length > 60;

/* Question 3: Write a query that captures the actor id, full name of the actor, and counts the number of movies each actor has made. (HINT: Think about whether you should group by actor id or the full name of the actor.) Identify the actor who has made the maximum number movies. */
SELECT a.actor_id,
	   CONCAT(first_name, ' ', last_name) full_name,
	   COUNT(*) num_movies
FROM actor a
JOIN film_actor fa
ON a.actor_id = fa.actor_id
JOIN film f
ON f.film_id = fa.film_id
GROUP BY 1, 2
ORDER BY 3 DESC;

/*********************************************
Quiz: Practce Quiz #2
*********************************************/

/* Question 1: Write a query that displays a table with 4 columns: actor's full name, film title, length of movie, and a column name "filmlen_groups" that classifies movies based on their length. Filmlen_groups should include 4 categories: 1 hour or less, Between 1-2 hours, Between 2-3 hours, More than 3 hours.

Match the filmlen_groups with the movie titles in your result dataset. */
SELECT CONCAT(first_name, ' ', last_name) full_name,
	   f.title film_title,
	   f.length,
	   CASE WHEN f.length <= 60 THEN '1 hour or less'
	        WHEN f.length > 60 AND f.length <= 120 THEN 'Between 1-2 hours'
			WHEN f.length > 121 AND f.length <= 180 THEN 'Between 2-3 hours'
			ELSE 'More than 3 hours' END AS filmlen_groups
FROM actor a
JOIN film_actor fa
ON a.actor_id = fa.actor_id
JOIN film f
ON f.film_id = fa.film_id;

/*
Academy Dinosaur - 'Between 1-2 hours'
Color Philadelphia - 'Between 2-3 hours'
Oklahoma Jumanji - '1 hour or less'
*/

/* Question 2: Now, we bring in the advanced SQL query concepts! Revise the query you wrote above to create a count of movies in each of the 4 filmlen_groups: 1 hour or less, Between 1-2 hours, Between 2-3 hours, More than 3 hours.

Match the count of movies in each filmlen_group. */

WITH sub AS (
	SELECT f.title film_title,
		   CASE WHEN f.length <= 60 THEN '1 hour or less'
				WHEN f.length > 60 AND f.length <= 120 THEN 'Between 1-2 hours'
				WHEN f.length > 120 AND f.length <= 180 THEN 'Between 2-3 hours'
				ELSE 'More than 3 hours' END AS filmlen_groups
	FROM film f)
	
SELECT filmlen_groups,
	   COUNT(*) num_movies
FROM sub
GROUP BY 1
ORDER BY 1;

/*
1 hour or less - 104
Betwen 1-2 hours - 439
Between 2-3 hours - 418
More than 3 hours - 39
*/

/*********************************************
Quiz: Question Set #1
*********************************************/

/* Question 1: We want to understand more about the movies that families are watching. The following categories are considered family movies: Animation, Children, Classics, Comedy, Family and Music.

Create a query that lists each movie, the film category it is classified in, and the number of times it has been rented out. */

WITH family_categories AS (
	SELECT f.film_id,
	       c.name category
	FROM category c
	JOIN film_category f
	ON c.category_id = f.category_id
	WHERE name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')),

  film_rentals AS (
	SELECT f.film_id,
	       f.title,
	       COUNT(*) num_rentals
	FROM film f
	JOIN inventory i
	ON f.film_id = i.film_id
	JOIN rental r
    ON i.inventory_id = r.inventory_id
    GROUP BY 1, 2)

SELECT f_rentals.title,
       f_categories.category,
	   f_rentals.num_rentals
FROM family_categories f_categories
JOIN film_rentals f_rentals
ON f_categories.film_id = f_rentals.film_id
ORDER BY 2, 1;

/* Question 2: Now we need to know how the length of rental duration of these family-friendly movies compares to the duration that all movies are rented for. Can you provide a table with the movie titles and divide them into 4 levels (first_quarter, second_quarter, third_quarter, and final_quarter) based on the quartiles (25%, 50%, 75%) of the rental duration for movies across all categories? Make sure to also indicate the category that these family-friendly movies fall into. */
SELECT f.title,
       c.name AS category,
	   f.rental_duration,
	   NTILE(4) OVER (ORDER BY rental_duration) standard_quartile
FROM category c
JOIN film_category fc
ON c.category_id = fc.category_id
JOIN film f
ON f.film_id = fc.film_id
ORDER BY 4;

/* Question 3: Finally, provide a table with the family-friendly film category, each of the quartiles, and the corresponding count of movies within each combination of film category for each corresponding rental duration category. The resulting table should have three columns:
    - Category
    - Rental length category
    - Count
*/
WITH quartile AS (
	SELECT c.name AS category,
		   f.rental_duration,
		   NTILE(4) OVER (ORDER BY rental_duration) standard_quartile
	FROM category c
	JOIN film_category fc
	ON c.category_id = fc.category_id
	JOIN film f
	ON f.film_id = fc.film_id
	WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')
	ORDER BY 3)

SELECT q.category,
	   q.standard_quartile,
	   COUNT(*)
FROM quartile q
GROUP BY 1, 2
ORDER BY 1, 2;

/*********************************************
Quiz: Question Set #2
*********************************************/

/* Question 1: We want to find out how the two stores compare in their count of rental orders during every month for all the years we have data for. Write a query that returns the store ID for the store, the year and month and the number of rental orders each store has fulfilled for that month. Your table should include a column for each of the following: year, month, store ID and count of rental orders fulfilled during that month. */

SELECT DATE_PART('month', r.rental_date) rental_month,
	   DATE_PART('year', r.rental_date) rental_year,
	   i.store_id,
	   COUNT(*) count_rentals
FROM rental r
JOIN inventory i
ON i.inventory_id = r.inventory_id
GROUP BY 1, 2, 3
ORDER BY 4 DESC;

/* Question 2: We would like to know who were our top 10 paying customers, how many payments they made on a monthly basis during 2007, and what was the amount of the monthly payments. Can you write a query to capture the customer name, month and year of payment, and total payment amount for each month by these top 10 paying customers? */

WITH top_customers AS (
	SELECT customer_id,
		   SUM(amount) total_payments
	FROM payment
	GROUP BY 1
	ORDER BY 2 DESC
	LIMIT 10),
	
  top_customer_payments AS (
	SELECT DATE_TRUNC('month', p.payment_date) AS pay_mon,
		   t.customer_id,
		   COUNT(*) AS pay_countpermon,
		   SUM(amount) AS pay_amount
	FROM top_customers t
	JOIN payment p
	ON t.customer_id = p.customer_id
	WHERE DATE_PART('year', p.payment_date) = 2007
	GROUP BY 1, 2)

SELECT t.pay_mon,
       CONCAT(c.first_name, ' ', c.last_name) fullname,
	   t.pay_countpermon,
	   t.pay_amount
FROM top_customer_payments t
JOIN customer c
ON t.customer_id = c.customer_id
ORDER BY 2, 1;

/* Question 3: Finally, for each of these top 10 paying customers, I would like to find out the difference across their monthly payments during 2007. Please go ahead and write a query to compare the payment amounts in each successive month. Repeat this for each of these 10 paying customers. */

WITH top_customers AS (
	SELECT customer_id,
		   SUM(amount) total_payments
	FROM payment
	GROUP BY 1
	ORDER BY 2 DESC
	LIMIT 10),
	
  top_customer_payments AS (
	SELECT DATE_TRUNC('month', p.payment_date) AS pay_mon,
		   CONCAT(c.first_name, ' ', c.last_name) fullname,
		   SUM(amount) AS pay_amount
	FROM top_customers t
	JOIN payment p
	ON t.customer_id = p.customer_id
	JOIN customer c
	ON t.customer_id = c.customer_id  
	WHERE DATE_PART('year', p.payment_date) = 2007
	GROUP BY 1, 2)

SELECT t.pay_mon,
       t.fullname,
	   t.pay_amount,
	   LAG(t.pay_amount) OVER (PARTITION BY t.fullname ORDER BY t.pay_mon) AS previous_month,
	   pay_amount - LAG(pay_amount) OVER (PARTITION BY fullname ORDER BY pay_mon) as month_difference
FROM top_customer_payments t
ORDER BY 2, 1;

/* Question 3 (Continued) - Also, it will be tremendously helpful if you can identify the customer name who paid the most difference in terms of payments. */

WITH top_customers AS (
	SELECT customer_id,
		   SUM(amount) total_payments
	FROM payment
	GROUP BY 1
	ORDER BY 2 DESC
	LIMIT 10),
	
  top_customer_payments AS (
	SELECT DATE_TRUNC('month', p.payment_date) AS pay_mon,
		   CONCAT(c.first_name, ' ', c.last_name) fullname,
		   SUM(amount) AS pay_amount
	FROM top_customers t
	JOIN payment p
	ON t.customer_id = p.customer_id
	JOIN customer c
	ON t.customer_id = c.customer_id  
	WHERE DATE_PART('year', p.payment_date) = 2007
	GROUP BY 1, 2)

SELECT *
FROM (SELECT t.pay_mon,
			 t.fullname,
			 t.pay_amount,
	  		 LAG(t.pay_amount) OVER (PARTITION BY t.fullname ORDER BY t.pay_mon) AS previous_month,
			 pay_amount - LAG(pay_amount) OVER (PARTITION BY fullname ORDER BY pay_mon) as month_difference
	  FROM top_customer_payments t
	  ORDER BY 2, 1) t3
WHERE t3.month_diff = (
	SELECT MAX(t1.month_diff)
	FROM (SELECT t.pay_mon,
				 t.fullname,
				 t.pay_amount,
				 LAG(t.pay_amount) OVER (PARTITION BY t.fullname ORDER BY t.pay_mon) AS previous_month,
				 pay_amount - LAG(t.pay_amount) OVER (PARTITION BY t.fullname ORDER BY t.pay_mon) as month_difference
		FROM top_customer_payments t
		ORDER BY 2, 1) t1);

/*
Written differently

WITH top_customers AS (
	SELECT customer_id,
		   SUM(amount) total_payments
	FROM payment
	GROUP BY 1
	ORDER BY 2 DESC
	LIMIT 10),
	
  top_customer_payments AS (
	SELECT DATE_TRUNC('month', p.payment_date) AS pay_mon,
		   CONCAT(c.first_name, ' ', c.last_name) fullname,
		   SUM(amount) AS pay_amount
	FROM top_customers t
	JOIN payment p
	ON t.customer_id = p.customer_id
	JOIN customer c
	ON t.customer_id = c.customer_id  
	WHERE DATE_PART('year', p.payment_date) = 2007
	GROUP BY 1, 2),
	
  lag_table AS (
	SELECT t.pay_mon,
	   	   t.fullname,
	 	   t.pay_amount,
		   LAG(t.pay_amount) OVER (PARTITION BY t.fullname ORDER BY t.pay_mon) AS previous_month,
	 	   pay_amount - LAG(pay_amount) OVER (PARTITION BY fullname ORDER BY pay_mon) as month_difference
	FROM top_customer_payments t)

SELECT *
FROM lag_table l1
WHERE l1.month_diff = (
	SELECT MAX(l2.month_diff)
	FROM lag_table l2);
*/