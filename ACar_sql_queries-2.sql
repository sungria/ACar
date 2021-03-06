SELECT r.vehicleid, r.ownerid,
           r.registrationnum,
           r."From",
           r."To",
           --o.name,
           --v.licence
    FROM registration AS r
    JOIN vehicle AS v ON vehicleid = v.id  
    JOIN owner AS o ON ownerid = o.id WHERE v.licence = 'BR512' AND o.name = 'Sungria';

ALTER TABLE vehicle RENAME licence TO vin;
ALTER TABLE vehicle ALTER COLUMN vin SET NOT NULL;
ALTER TABLE vehicle ADD CONSTRAINT constraint_unique UNIQUE (vin);

ALTER TABLE registration ALTER COLUMN registrationnum SET NOT NULL;

SELECT v.brand_id,
       v.model_id,
       r.registrationnum,
       --o.name,
       r."From",
       r."To"
FROM registration as r
JOIN vehicle AS v ON vehicleid = v.id 
JOIN owner as o ON ownerid = o.id

SELECT brand, model, year 
FROM 
   (SELECT v.vin,
       b.name as brand,
       m.name as model,
       m.year
   FROM brand as b
   JOIN model as m ON b.id = m.brand_id
   JOIN vehicle AS v ON v.model_id = m.id) AS sub
 WHERE vin = 'VV404';

SELECT name, regnum, "From", "To"
FROM (
    SELECT o.name, 
       r.registrationnum AS regnum,
       r."From",
       r."To",
       v.vin
    FROM registration AS r
    JOIN owner AS o ON o.id = r.ownerid
    JOIN vehicle AS v ON v.id = r.vehicleid) AS sub
 WHERE vin = 'AA123'

EXPLAIN
 WITH cte_reg AS (
    SELECT o.name, 
       r.registrationnum AS regnum,
       r."From",
       r."To",
       v.vin
    FROM registration AS r
    JOIN owner AS o ON o.id = r.ownerid
    JOIN vehicle AS v ON v.id = r.vehicleid)
    WHERE r."To" IS NULL

SELECT name, regnum, "From", "To"
FROM cte_reg
WHERE vin = 'AA123' AND "To" IS NULL;

UPDATE registration r
SET "To" = now()
FROM vehicle v
WHERE r.vehicleid = v.id AND v.vin = 'AA123' AND r."To" IS NULL;

ALTER TABLE registration DROP CONSTRAINT registration_pkey;
ALTER TABLE registration ADD PRIMARY KEY (registrationnum);

EXPLAIN SELECT b.name, m.name, oreg.name, oreg."From"
FROM (
   SELECT r.vehicleid, v.vin, o.name, r."From",
          v.brand_id, v.model_id 
   FROM registration r, vehicle v, owner o
   WHERE r."To" IS NULL
     AND r.vehicleid = v.id
     AND r.ownerid = o.id
     AND v.vin = 'AA123') AS oreg
 JOIN brand b ON b.id = oreg.brand_id
 JOIN model m ON m.id = oreg.model_id;

ALTER TABLE registration DROP CONSTRAINT registration_pkey;
ALTER TABLE registration ADD PRIMARY KEY (vehicleid, ownerid, "From");
 


   