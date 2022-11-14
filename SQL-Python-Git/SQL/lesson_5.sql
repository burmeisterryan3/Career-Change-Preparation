/*
Methods for data cleaning. Techniques include parsing information, returning where the information lives, and changing the type of the information.
Left: Extracts a number of characters from a string starting from the left
Right: Extracts a number of characters from a string starting from the right
Substr: Extracts a substring from a string (starting at any position)
Position: Returns the position of the first occurrence of a substring in a string
Strpos: Returns the position of a substring within a string
Concat: Adds two or more expressions together
Cast: Converts a value of any type into a specific, different data type
Coalesce: Returns the first non-null value in a list

Left/Right/Substr: Used to extract information typically when all information resides in a single column
Concat: Used commonly when two or more pieces of information can be used as a unique identifier
Cast: Used when data types default to a specific type (e.g., most commonly STRING) and need to be assigned to the appropriate data type to run computations

Advanced Cleaning Functions
Position/Strpos: Used to return the position of information to identify where relevant information is held in a string to then extract across all records
Coalesce: Used to return the first non-null value that’s commonly used for normalizing data that’s stretched across multiple columns and includes NULLs
*/

/*********************************************
Quiz: LEFT & RIGHT Quiz
*********************************************/

/* Question 1: In the accounts table, there is a column holding the website for each company. The last three digits specify what type of web address they are using. A list of extensions (and pricing) is provided here. Pull these extensions and provide how many of each website type exist in the accounts table. */
SELECT RIGHT(website, 3), COUNT(*)
FROM accounts
GROUP BY 1
ORDER BY 1;

/* Question 2: There is much debate about how much the name (or even the first letter of a company name) matters. Use the accounts table to pull the first letter of each company name to see the distribution of company names that begin with each letter (or number). */
WITH first_char AS(
  SELECT LEFT(name, 1) f_char
  FROM accounts)

SELECT LEFT(name, 1), COUNT(*)
FROM accounts
GROUP BY 1
ORDER BY 2 DESC;

/* Question 3: Use the accounts table and a CASE statement to create two groups: one group of company names that start with a number and the second group of those company names that start with a letter. What proportion of company names start with a letter? */
WITH first_char AS (
  	SELECT LEFT(name, 1) f_char
  	FROM accounts)

SELECT CASE WHEN f_char ~ '[a-zA-Z]' THEN 'letter'
            ELSE 'number' END AS let_or_num,
        COUNT(*)
FROM first_char
GROUP BY 1;

/* Question 4: Consider vowels as a, e, i, o, and u. What proportion of company names start with a vowel, and what percent start with anything else? */
WITH first_char AS (
  	SELECT LEFT(name, 1) f_char
  	FROM accounts)

SELECT CASE WHEN UPPER(f_char) IN ('A', 'E', 'I', 'O', 'U') THEN 'vowel'
            ELSE 'other' END AS vowel_or_not,
        COUNT(*)
FROM first_char
GROUP BY 1;

/* REGEX
WITH first_char AS (
  	SELECT LEFT(name, 1) f_char
  	FROM accounts)

SELECT CASE WHEN f_char ~ '^[aeiouAEIOU]' THEN 'vowel'
            ELSE 'other' END AS vowel_or_not,
        COUNT(*)
FROM first_char
GROUP BY 1;
*/

/*********************************************
Quiz: CONCAT Quiz
*********************************************/

/* Question 1: Suppose the company wants to assess the performance of all the sales representatives. Each sales representative is assigned to work in a particular region. To make it easier to understand for the HR team, display the concatenated sales_reps.id, ‘_’ (underscore), and region.name as EMP_ID_REGION for each sales representative. */
SELECT CONCAT(s.name, '_', r.name) emp_id_region
FROM sales_reps s
JOIN region r
ON r.id = s.region_id;

/* Question 2: From the accounts table, display the name of the client, the coordinate as concatenated (latitude, longitude), email id of the primary point of contact as <first letter of the primary_poc><last letter of the primary_poc>@<extracted name and domain from the website>. */
SELECT a.name, CONCAT(lat, ', ', long), CONCAT(LEFT(primary_poc, 1), RIGHT(primary_poc, 1), '@', SUBSTR(website, 5)) email
FROM accounts;

/* Question 3: From the web_events table, display the concatenated value of account_id, '_' , channel, '_', count of web events of the particular channel. */
WITH ch_ct AS (
  SELECT account_id, channel, COUNT(*) ch_ct
  FROM web_events
  GROUP BY account_id, channel)

SELECT CONCAT(account_id, '_', channel, '_', ch_ct)
FROM ch_ct;

/*********************************************
Quiz: CAST Quiz
*********************************************/

/* Question 1: Write a query to look at the top 10 rows to understand the columns and the raw data in the dataset called sf_crime_data. */
SELECT *
FROM sf_crime_data
LIMIT 10;

/* Question 2: Remembering back to the lesson on dates, use the Quiz Question at the bottom of this page to make sure you remember the format that dates should use in SQL.
   SOLUTION: yyyy-mm-dd */

/* Question 3: Look at the date column in the sf_crime_data table. Notice the date is not in the correct format. */

/* Question 4: Write a query to change the date in to the correct SQL date format. You will need to use at least SUBSTR and CONCAT to perform this operation. */
SELECT *, CONCAT(SUBSTR(date, 7, 4), '-', SUBSTR(date, 1, 2), '-', SUBSTR(date, 4, 2)) AS n_date
FROM sf_crime_data;

/*
Solution provided: 

SELECT date orig_date, (SUBSTR(date, 7, 4) || '-' || LEFT(date, 2) || '-' || SUBSTR(date, 4, 2)) new_date
FROM sf_crime_data; */


/* Question 5: Once you have created a column in the correct format, use either CAST or :: to convert this to a date. */
SELECT *, CAST(CONCAT(SUBSTR(date, 7, 4), '-', SUBSTR(date, 1, 2), '-', SUBSTR(date, 4, 2)) AS date) AS n_date
FROM sf_crime_data;

/*
Solution provided:

SELECT date orig_date, (SUBSTR(date, 7, 4) || '-' || LEFT(date, 2) || '-' || SUBSTR(date, 4, 2))::DATE new_date
FROM sf_crime_data; */

/*
POSTION, STRPOS Examples

student_information
2838581,F,san francisco,3.7,$1000000
2842940,M,chicago,3.8,$150000
28492940,F,new york city,3.9,$200000
284922019,M,boston,3.5,$125000

POSITION("$" IN student_information) as
salary_starting_position

-> Could be used for SUBSTR(student_information, POSITION("$" IN student_information)) to retrieve salary when the position varies across entries */

/*********************************************
Quiz: POSTION & STRPOS Quiz
*********************************************/

/* Question 1: Use the accounts table to create first and last name columns that hold the first and last names for the primary_poc. */
SELECT LEFT(primary_poc, POSITION(' ' IN primary_poc)-1) AS first_name,
       SUBSTR(primary_poc, POSITION(' ' IN primary_poc)) AS last_name
FROM accounts;

/*
Solution provided:

SELECT LEFT(primary_poc, STRPOS(primary_poc, ' ') -1 ) first_name, 
RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')) last_name
FROM accounts;
*/

/* Question 2: Now see if you can do the same thing for every rep name in the sales_reps table. Again provide first and last name columns. */
SELECT LEFT(name, POSITION(' ' IN name)-1) AS first_name,
       SUBSTR(name, POSITION(' ' IN name)) AS last_name
FROM sales_reps;

/*
Solution provided:

SELECT LEFT(name, STRPOS(name, ' ') -1 ) first_name, 
       RIGHT(name, LENGTH(name) - STRPOS(name, ' ')) last_name
FROM sales_reps;
*/

/*********************************************
Quiz: CONCAT & STRPOS Quiz
*********************************************/

/* Question 1: Each company in the accounts table wants to create an email address for each primary_poc. The email address should be the first name of the primary_poc . last name primary_poc @ company name .com. */
SELECT CONCAT(LEFT(primary_poc, STRPOS(primary_poc, ' ')-1), '.', RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')), '@', name, '.com') email
FROM accounts;

/*
Solution provided:

WITH t1 AS (
 SELECT LEFT(primary_poc, STRPOS(primary_poc, ' ')-1) first_name,
        RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')) last_name,
        name
 FROM accounts)
SELECT first_name, last_name, CONCAT(first_name, '.', last_name, '@', name, '.com')
FROM t1;
*/

/* Question 2: You may have noticed that in the previous solution some of the company names include spaces, which will certainly not work in an email address. See if you can create an email address that will work by removing all of the spaces in the account name, but otherwise, your solution should be just as in question 1. Some helpful documentation is here. */
SELECT REPLACE(CONCAT(LEFT(primary_poc, STRPOS(primary_poc, ' ')-1), '.', RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')), '@', name, '.com'), ' ', '') email
FROM accounts;

/*
Solution provided:

WITH t1 AS (
 SELECT LEFT(primary_poc, STRPOS(primary_poc, ' ') -1 ) first_name,
        RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')) last_name,
        name
 FROM accounts)
SELECT first_name, last_name, CONCAT(first_name, '.', last_name, '@', REPLACE(name, ' ', ''), '.com')
FROM  t1;
*/

/* Question 3: We would also like to create an initial password, which they will change after their first log in. The first password will be the first letter of the primary_poc's first name (lowercase), then the last letter of their first name (lowercase), the first letter of their last name (lowercase), the last letter of their last name (lowercase), the number of letters in their first name, the number of letters in their last name, and then the name of the company they are working with, all capitalized with no spaces. */
SELECT CONCAT(LOWER(LEFT(primary_poc, 1)),
              LOWER(SUBSTR(primary_poc, STRPOS(primary_poc, ' ')-1, 1)),
              LOWER(SUBSTR(primary_poc, STRPOS(primary_poc, ' ')+1, 1)),
              LOWER(RIGHT(primary_poc, 1)),
              STRPOS(primary_poc, ' ')-1,
              LENGTH(primary_poc)-STRPOS(primary_poc, ' '),
              REPLACE(UPPER(name), ' ', ''))
FROM accounts;

/*
Solution provided:

WITH t1 AS (
 SELECT LEFT(primary_poc, STRPOS(primary_poc, ' ') -1 ) first_name,
        RIGHT(primary_poc, LENGTH(primary_poc) - STRPOS(primary_poc, ' ')) last_name,
        name
 FROM accounts)
SELECT first_name,
       last_name,
       CONCAT(first_name, '.', last_name, '@', name, '.com'),
       LEFT(LOWER(first_name), 1) || RIGHT(LOWER(first_name), 1) || LEFT(LOWER(last_name), 1) || RIGHT(LOWER(last_name), 1) || LENGTH(first_name) || LENGTH(last_name) || REPLACE(UPPER(name), ' ', '')
FROM t1;
*/

/*
COALESCE Example - Wages will only be 1 of the following: hourly, salaray, or sales - Coalesce allows us to shift to a common assessment of salary

hourly_wage | salary | sales
8 | null | null
null | 150,000 | null
7 | null | null
null | 200,000 | null
null | null | 100
null | null | 200

COALESCE(hourly_wage*40*52, salary, commission*sales) AS annual_income

The three methods below are the most common ways to deal with null values in SQL:

Coalesce: Allows you to return the first non-null value across a set of columns in a slick, single command. This is a good approach only if a single column’s value needs to be extracted whilst the rest are null.
Drop records: Sometimes, if there are null values in records at all, analysts can decide to drop the row entirely. This is not favorable, as it removes data. Data is precious. Think about the reason those values are null. Does it make sense to use COALESCE, drop records, and conduct an imputation.
Imputation: Outside of the COALESCE use case, you may want to impute missing values. If so, think about the problem you are trying to solve, and impute accordingly. Perhaps you’d like to be conversative so you take the MIN of that column or the 25th percentile value. Classic imputation values are often the median or mean value of the column.
*/

/*********************************************
Quiz: COALESCE Quiz
*********************************************/

/* Question 1: Run the query entered below in the SQL workspace to notice the missing data. */
SELECT *
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;

/* Question 2: Use COALESCE to fill in the accounts.id column with the account.id for the NULL value for table in 1. */
SELECT *, COALESCE(a.id, a.id) id, COALESCE(a.id, a.id) account_id
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;

/* Question 3: Use COALESCE to fill in the orders.account_id column with the account.id for the NULL value for the table in 1. */
SELECT *, COALESCE(a.id, a.id) id, COALESCE(a.id, a.id) account_id
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;

/* Question 4: Use COALESCE to filli in each of the qty and usd columns with 0 for the table in 1. */
SELECT COALESCE(a.id, a.id) filled_id,
       a.name,
       a.website,
       a.lat,
       a.long,
       a.primary_poc,
       a.sales_rep_id,
       COALESCE(o.account_id, a.id) account_id,
       o.occurred_at,
       COALESCE(o.standard_qty, 0) standard_qty,
       COALESCE(o.gloss_qty,0) gloss_qty,
       COALESCE(o.poster_qty,0) poster_qty,
       COALESCE(o.total,0) total,
       COALESCE(o.standard_amt_usd,0) standard_amt_usd,
       COALESCE(o.gloss_amt_usd,0) gloss_amt_usd,
       COALESCE(o.poster_amt_usd,0) poster_amt_usd,
       COALESCE(o.total_amt_usd,0) total_amt_usd
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;

/* Question 5: Run the query in 1 with the WHERE removed and COUNT the numer of ids. */
SELECT COUNT(*)
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id;

/* Question 5: Run the query in 5 but with the COALESCE function used in questions 2 through 4. */
SELECT COALESCE(a.id, a.id) filled_id,
       a.name,
       a.website,
       a.lat,
       a.long,
       a.primary_poc,
       a.sales_rep_id,
       COALESCE(o.account_id, a.id) account_id,
       o.occurred_at,
       COALESCE(o.standard_qty, 0) standard_qty,
       COALESCE(o.gloss_qty,0) gloss_qty,
       COALESCE(o.poster_qty,0) poster_qty,
       COALESCE(o.total,0) total,
       COALESCE(o.standard_amt_usd,0) standard_amt_usd,
       COALESCE(o.gloss_amt_usd,0) gloss_amt_usd,
       COALESCE(o.poster_amt_usd,0) poster_amt_usd,
       COALESCE(o.total_amt_usd,0) total_amt_usd
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id;

/*
Final COALESCE example:

Product | Unit_price | Num_in_stock | Num_ordered
a | 2.00 | 10 | 5
b | 2.50 | 15 | 
c | 3.00 | 20 | 10
d | 3.50 | 25 | 

SELECT product, unit+price*(num_in_stock + COALESCE(num_ordered, 0)) FROM product_db;
*/