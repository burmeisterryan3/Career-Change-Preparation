/*********************************************
				  Slide 1
*********************************************/
WITH customer_country AS (
	SELECT co.country, cu.customer_id
	FROM country co
	JOIN city ci
	ON co.country_id = ci.country_id
	JOIN address a
	ON ci.city_id = a.city_id
	JOIN customer cu
	ON a.address_id = cu.customer_id),

  country_orders_month AS (
	SELECT DATE_PART('month', r.rental_date) rental_month,
	 	   DATE_PART('year', r.rental_date) rental_year,
	   	   c.country,
	   	   COUNT(*) num_orders
	FROM customer_country c
	JOIN rental r
	ON r.customer_id = c.customer_id
	WHERE DATE_PART('year', r.rental_date) = 2005
	GROUP BY 1, 2, 3),

  top_countries AS (
	SELECT c.country,
	   	   COUNT(*) num_orders
	FROM customer_country c
	JOIN rental r
	ON r.customer_id = c.customer_id
  	WHERE DATE_PART('year', r.rental_date) = 2005
	GROUP BY 1
  	ORDER BY 2 DESC
  	LIMIT 5)

/* Create pivot table */
SELECT CASE WHEN rental_month = 5 THEN '5 - May'
            WHEN rental_month = 6 THEN '6 - June'
			WHEN rental_month = 7 THEN '7- July'
			WHEN rental_month = 8 THEN '8 - August' END AS rental_date,
	   MAX(CASE WHEN (c.country = 'China') THEN c.num_orders ELSE NULL END) AS china,
	   MAX(CASE WHEN (c.country = 'India') THEN c.num_orders ELSE NULL END) AS india,
	   MAX(CASE WHEN (c.country = 'United States') THEN c.num_orders ELSE NULL END) AS united_states,
	   MAX(CASE WHEN (c.country = 'Japan') THEN c.num_orders ELSE NULL END) AS japan,
	   MAX(CASE WHEN (c.country = 'Mexico') THEN c.num_orders ELSE NULL END) AS mexico
FROM country_orders_month c
JOIN top_countries t
ON t.country = c.country
GROUP BY 1
ORDER BY 1;

/*********************************************
                  Slide 2
*********************************************/
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

  /* Create pivot table for the top paying customers */
  pivot_table AS (
	SELECT CASE WHEN DATE_PART('month', t.pay_mon) = 2 THEN '2 - Feb'
				WHEN DATE_PART('month', t.pay_mon) = 3 THEN '3 - Mar'
				WHEN DATE_PART('month', t.pay_mon) = 4 THEN '4 - Apr'
				WHEN DATE_PART('month', t.pay_mon) = 5 THEN '5 - May' END AS rental_month,
		   MAX(CASE WHEN (t.fullname = 'Ana Bradley') THEN t.pay_amount ELSE NULL END) AS ana_bradley,
		   MAX(CASE WHEN (t.fullname = 'Clara Shaw') THEN t.pay_amount ELSE NULL END) AS clara_Shaw,
		   MAX(CASE WHEN (t.fullname = 'Curtis Irby') THEN t.pay_amount ELSE NULL END) AS curtis_irby,
		   MAX(CASE WHEN (t.fullname = 'Eleanor Hunt') THEN t.pay_amount ELSE NULL END) AS eleanor_hunt,
		   MAX(CASE WHEN (t.fullname = 'Karl Seal') THEN t.pay_amount ELSE NULL END) AS karl_seal,
		   MAX(CASE WHEN (t.fullname = 'Marcia Dean') THEN t.pay_amount ELSE NULL END) AS marcia_dean,
		   MAX(CASE WHEN (t.fullname = 'Marion Snyder') THEN t.pay_amount ELSE NULL END) AS marion_snyder,
		   MAX(CASE WHEN (t.fullname = 'Mike Way') THEN t.pay_amount ELSE NULL END) AS mike_way,
		   MAX(CASE WHEN (t.fullname = 'Rhonda Kennedy') THEN t.pay_amount ELSE NULL END) AS rhonda_kennedy,
		   MAX(CASE WHEN (t.fullname = 'Tommy Collazo') THEN t.pay_amount ELSE NULL END) AS tommy_collazo
	FROM top_customer_payments t
	GROUP BY 1)

/* Change NULL values, caused by a lack of rentals by an individual in a particular month, to zero for plotting purposes */
SELECT rental_month,
	   CASE WHEN ana_bradley IS NULL THEN 0
			ELSE ana_bradley END AS ana_bradley,
	   CASE WHEN clara_shaw IS NULL THEN 0
			ELSE clara_shaw END AS clara_shaw,
	   CASE WHEN curtis_irby IS NULL THEN 0
			ELSE curtis_irby END AS curtis_irby,
	   CASE WHEN eleanor_hunt IS NULL THEN 0
			ELSE eleanor_hunt END AS eleanor_hunt,
	   CASE WHEN karl_seal IS NULL THEN 0
			ELSE karl_seal END AS karl_seal,
	   CASE WHEN marcia_dean IS NULL THEN 0
			ELSE marcia_dean END AS marcia_dean,
	   CASE WHEN marion_snyder IS NULL THEN 0
			ELSE marion_snyder END AS marion_snyder,
	   CASE WHEN mike_way IS NULL THEN 0
			ELSE mike_way END AS mike_way,
	   CASE WHEN rhonda_kennedy IS NULL THEN 0
			ELSE rhonda_kennedy END AS rhonda_kennedy,
	   CASE WHEN tommy_collazo IS NULL THEN 0
			ELSE tommy_collazo END AS tommy_collazo
FROM pivot_table
ORDER BY 1;

/*********************************************
                  Slide 3
*********************************************/
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
	ORDER BY 3),

  quartile_count AS (
    SELECT q.category,
           q.standard_quartile,
           COUNT(*) ct
    FROM quartile q
    GROUP BY 1, 2
    ORDER BY 1, 2)

/* Create pivot table */
SELECT category,
       MAX(CASE WHEN standard_quartile = 1 THEN ct ELSE NULL END) AS first,
       MAX(CASE WHEN standard_quartile = 2 THEN ct ELSE NULL END) AS second,
       MAX(CASE WHEN standard_quartile = 3 THEN ct ELSE NULL END) AS third,
       MAX(CASE WHEN standard_quartile = 4 THEN ct ELSE NULL END) AS fourth
FROM quartile_count
GROUP BY category
ORDER BY 1;

/*********************************************
                  Slide 4
*********************************************/
WITH store_rentals AS (
	SELECT DATE_PART('month', r.rental_date) rental_month,
		   DATE_PART('year', r.rental_date) rental_year,
		   i.store_id,
		   COUNT(*) count_rentals
	FROM rental r
	JOIN inventory i
	ON i.inventory_id = r.inventory_id
	GROUP BY 1, 2, 3
	ORDER BY 4 DESC)

/* Create pivot table */
SELECT rental_year || '-' || rental_month AS rental_month,
	   MAX(CASE WHEN store_id = 1 THEN count_rentals ELSE NULL END) AS one,
	   MAX(CASE WHEN store_id = 2 THEN count_rentals ELSE NULL END) AS two
FROM store_rentals
GROUP BY 1
ORDER BY 1;
