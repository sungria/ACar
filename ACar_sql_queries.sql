ACar queries:

-- I did it in UI
CREATE SEQUENCE public.model_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE public.model_id_seq
  OWNER TO postgres;

ALTER TABLE tire ALTER COLUMN id SET DEFAULT nextval('model_id_seq'::regclass); 

-- auto increment (not vehicle :)
INSERT INTO brand (name)
VALUES ('BMW'),
       ('Suzuki'),
       ('GT'),
       ('eBike');

INSERT INTO model (brand_id, name, year)
VALUES 
    (1, 'X5', '2010-07-14'),
    (...)... -- I forgot it :)

-- change the property of the column in the table
ALTER TABLE vehicle ALTER COLUMN towing DROP NOT NULL;

ALTER TABLE vehicle ALTER COLUMN doors DROP NOT NULL;

INSERT INTO type (id)
VALUES 
    ('car'),
    ('bike'),
    ('ebike');

INSERT INTO owner (name)
VALUES 
    ('P3'),
    ('Sungria'),
    ('Panic Monster');

SELECT b.id, b.name, m.id, m.name, count(v.*)
  FROM brand AS b
  JOIN model AS m ON m.brand_id = b.id
  LEFT JOIN vehicle AS v ON v.brand_id = m.brand_id AND v.model_id = m.id
 GROUP BY b.id, b.name, m.id, m.name

INSERT INTO vehicle(brand_id, model_id, "type")
-- VALUES (m.brand_id, m.id, "car")
SELECT m.brand_id, m.id, 'car'
  FROM brand AS b
  JOIN model AS m ON m.brand_id = b.id
 WHERE b.name = 'BMW' AND m.name = 'X5';

 COMMIT;

INSERT INTO wheel(vehicle_id, susspringrate, braketype, wheeldiameter)
VALUES 
    (1, 3, 'break!', 16),
    (3, 2, 'bb8', 18); 

SELECT b.id, b.name, m.id, m.name, count(v.*)
  FROM brand AS b
  JOIN model AS m ON m.brand_id = b.id
  LEFT JOIN vehicle AS v ON v.brand_id = m.brand_id AND v.model_id = m.id
 GROUP BY b.id, b.name, m.id, m.name;

INSERT INTO vehicle(brand_id, model_id, "type")
-- VALUES (m.brand_id, m.id, "car")
SELECT m.brand_id, m.id, 'car'
  FROM brand AS b
  JOIN model AS m ON m.brand_id = b.id
 WHERE b.name = 'Suzuki' AND m.name = 'Swift';

ALTER TABLE tire ALTER COLUMN id SET DEFAULT nextval('tire_id_seq'::regclass); 

INSERT INTO tire(vehicle_id, wheel_id, width, airpressure, type)
VALUES 
    (2, 3, 155, 1.6, 'summer');
    --(1, 1, 165, 2.0, 'winter'); 

ALTER TABLE vehicle ADD COLUMN licence character varying(255);

INSERT INTO engine(vehicle_id, capacity, numberofcylinders, power)
SELECT --VALUES 
    v.id, 1.6, 6, 120    
  FROM vehicle as v
  --JOIN brand AS b
  --JOIN model AS m ON m.brand_id = b.id
  WHERE v.licence='AA123'; 

UPDATE vehicle
SET licence ='BR512' WHERE id = 5;


-- Registration starts here
INSERT INTO registration(vehicleid, ownerid, registrationnum, "From")
SELECT 
   v.id, o.id, 000333, '2011-04-22'
   FROM vehicle AS v , owner as o
   WHERE v.licence = 'BR512' AND o.name = 'P3';
 --COMMIT;

-- Not correct: UPDATE old one "To" and INSERT new one to keep the history.
-- UPDATE registration 
-- SET vehicleid = '1'
-- WHERE ownerid = '1'

INSERT INTO registration(vehicleid, ownerid, registrationnum, "From")
SELECT 
   v.id, o.id, 444, now()
   FROM vehicle AS v , owner as o
   WHERE v.licence = 'VV404' AND o.name = 'Sungria';
-- here the license doesn't make sense... 


-- TODO: ad all the columns like name and car info
 SELECT vehicleid, ownerid,
           registrationnum,
           "From",
           "To"
    FROM registration
    JOIN vehicle AS v ON vehicleid = v.id WHERE v.licence = 'BR512';

-- ad all the columns like name and car info
SELECT vehicleid, ownerid,
           registrationnum,
           "From",
           "To"
    FROM registration
    JOIN vehicle AS v ON vehicleid = v.id --WHERE v.licence = 'BR512' 
    JOIN owner AS o ON ownerid = o.id WHERE v.licence = 'BR512' AND o.name = 'Sungria';


INSERT INTO registration(vehicleid, ownerid, registrationnum, "From")
SELECT 
   v.id, o.id, 444, now()
   FROM vehicle AS v , owner as o
   WHERE v.licence = 'VV404' AND o.name = 'Sungria';

SELECT vehicleid, ownerid,
           registrationnum,
           "From",
           "To"
    FROM registration
    JOIN vehicle AS v ON vehicleid = v.id --WHERE v.licence = 'BR512' 
    JOIN owner AS o ON ownerid = o.id WHERE v.licence = 'BR512' AND o.name = 'Sungria';


