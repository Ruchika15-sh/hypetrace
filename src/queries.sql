-- 1.Celebrity/controversy events with brand names
SELECT
b.brand_name,
e.celebrity,
e.event_date,
e.event_type,
e.occasion
FROM events e
JOIN brands b ON e.brand_id = b.brand_id
ORDER BY e.event_date;

-- 2.Rolling average of search interest per band for 4 weeks
SELECT
      b.brand_name,
	  t.date,
	  t.search_interest,
	  ROUND(AVG(t.search_interest) OVER(
	  PARTITION BY t.brand_id
	  ORDER BY t.date
	  ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
	  ), 2) AS rolling_4wk_avg
FROM trend_metrics t
JOIN brands b 
ON t.brand_id = b.brand_id
ORDER BY b.brand_name, t.date;

-- 3.Brand Popularity ranking by average search interest 
SELECT
      b.brand_name,
	  ROUND(AVG(t.search_interest), 2) AS avg_search_interest,
	  RANK() OVER (ORDER BY AVG(t.search_interest)DESC) AS popularity_rank
FROM trend_metrics t
JOIN brands b
ON t.brand_id = b.brand_id
GROUP BY b.brand_name
ORDER BY popularity_rank;