-- https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions/

-- Solution 1: NOT IN
/*
SELECT
    customer_id, 
    COUNT(visit_id) AS count_no_trans 
FROM 
    visits 
WHERE 
    visit_id NOT IN (
        SELECT 
            visit_id
        FROM 
            transactions
    ) 
GROUP BY 
  customer_id
;
*/

-- Solution 2: IS NULL
SELECT
    customer_id,
    COUNT(*) AS count_no_trans
FROM
    visits AS v
    LEFT JOIN transactions AS t ON v.visit_id = t.visit_id
WHERE
    t.visit_id IS NULL
GROUP BY
    customer_id
;