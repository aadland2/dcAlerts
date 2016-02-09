-- CREATE TABLE alerts (tweet_id bigint,created_at timestamp,body text, type text,symbol text,lat float,lon float;
-- create extension postgis;
-- ALTER TABLE alerts ADD COLUMN geom geometry(POINT,4326);
-- UPDATE alerts SET geom = ST_SetSRID(ST_MakePoint(lon,lat),4326); 


--- Row to JSON Selection
-- SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features
--         FROM (SELECT 'Feature' As type
--         , ST_AsGeoJSON(lg.geom)::json As geometry
--         , row_to_json((SELECT l FROM (SELECT body,symbol) As l
--         )) As properties
--         FROM alerts As lg  ) As f )  As fc;
