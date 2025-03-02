SELECT 
    COALESCE (f.currency_id , NULL) AS currency_id,
    COALESCE (f.currency , NULL) AS currency,
    COALESCE (f.updated_at , NULL) AS updated_at,
    COALESCE (f.amount , NULL) AS amount
FROM file('./currency.csv', 'CSV') AS f