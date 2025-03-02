SELECT * FROM {{ref('staging_dbjobs_vnw')}}
UNION ALL
SELECT * FROM {{ref('staging_dbjobs_crv')}}
UNION ALL
SELECT * FROM {{ref('staging_dbjobs_jbk')}}