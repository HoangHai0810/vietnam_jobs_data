WITH dc AS (
    SELECT *
    FROM {{ref('staging_currency')}}
)
SELECT
modify_job_title(job_title) AS job_title,
check_null_currency(get_salary_lower_bound(salary)) * dc.amount AS salary_lowerbound,
check_null_currency(get_salary_upper_bound(salary)) * dc.amount AS salary_upperbound,
lower(normalizeArray(skills)) AS skills,
level AS level,
normalizeArray(category) AS category,
extractNumberFromText(min_yoe) AS min_yoe,
normalizeArray(benefits) AS benefits,
--- AS addresss
--- AS district
--- AS province
company_name AS company_name,
CASE
    WHEN (extractSecondNumberFromText(company_size) >= 1000)
        THEN 'Large'
    WHEN (extractSecondNumberFromText(company_size) >= 400)
        THEN 'Big'
    WHEN (extractSecondNumberFromText(company_size) >= 50)
        THEN 'Medium'
    WHEN (extractSecondNumberFromText(company_size) >= 0)
        THEN 'Small'
    ELSE 'Unknown' END as company_size,
    source AS source,
CASE
    WHEN (extractNumberFromText(views) >= 5000)
        THEN 'Trending'
    WHEN (extractNumberFromText(views) >= 1000)
        THEN 'Popular'
    WHEN (extractNumberFromText(views) >= 500)
        THEN 'Moderate'
    WHEN (extractNumberFromText(views) >= 0)
        THEN 'Low'
    ELSE 'Unknown' END as views,
    toDate(parseDateTimeBestEffortOrNull(due_date)) AS due_date
FROM 
    raw_dbjobs.raw_dbjobs_crv
    LEFT JOIN dc
ON normalize_salary(salary) = dc.currency