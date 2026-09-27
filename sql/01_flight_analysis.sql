-- ============================================================
-- Flight Delay Analysis & Operational Insights
-- Dataset: January 2025 BTS On-Time Performance
-- ============================================================


-- 1. Total Scheduled Flights
SELECT
    COUNT(*) AS total_scheduled_flights
FROM flights;


-- 2. Cancelled Flights
SELECT
    COUNT(*) AS cancelled_flights
FROM flights
WHERE CANCELLED = '1.00';


-- 3. Diverted Flights
SELECT
    COUNT(*) AS diverted_flights
FROM flights
WHERE DIVERTED = '1.00';


-- 4. Operated Flights
SELECT
    COUNT(*) AS operated_flights
FROM flights
WHERE CANCELLED = '0.00'
  AND DIVERTED = '0.00'
  AND ARR_DELAY IS NOT NULL;


-- 5. Delayed Flights (15+ Minutes)
SELECT
    COUNT(*) AS delayed_flights
FROM flights
WHERE CANCELLED = '0.00'
  AND DIVERTED = '0.00'
  AND CAST(ARR_DELAY AS REAL) >= 15;


-- 6. Overall Delay Rate
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN CAST(ARR_DELAY AS REAL) >= 15 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS delay_rate_percent
FROM flights
WHERE CANCELLED = '0.00'
  AND DIVERTED = '0.00'
  AND ARR_DELAY IS NOT NULL;


-- 7. Delay Rate by Airline
SELECT
    OP_UNIQUE_CARRIER AS airline,
    COUNT(*) AS operated_flights,
    SUM(
        CASE
            WHEN CAST(ARR_DELAY AS REAL) >= 15 THEN 1
            ELSE 0
        END
    ) AS delayed_flights,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN CAST(ARR_DELAY AS REAL) >= 15 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS delay_rate_percent
FROM flights
WHERE CANCELLED = '0.00'
  AND DIVERTED = '0.00'
  AND ARR_DELAY IS NOT NULL
GROUP BY OP_UNIQUE_CARRIER
ORDER BY delay_rate_percent DESC;


-- 8. Delay Rate by Origin Airport
SELECT
    ORIGIN AS airport,
    COUNT(*) AS operated_flights,
    SUM(
        CASE
            WHEN CAST(ARR_DELAY AS REAL) >= 15 THEN 1
            ELSE 0
        END
    ) AS delayed_flights,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN CAST(ARR_DELAY AS REAL) >= 15 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS delay_rate_percent
FROM flights
WHERE CANCELLED = '0.00'
  AND DIVERTED = '0.00'
  AND ARR_DELAY IS NOT NULL
GROUP BY ORIGIN
HAVING COUNT(*) >= 500
ORDER BY delay_rate_percent DESC
LIMIT 20;


-- 9. Delay Rate by Route
SELECT
    ORIGIN || ' → ' || DEST AS route,
    COUNT(*) AS operated_flights,
    SUM(
        CASE
            WHEN CAST(ARR_DELAY AS REAL) >= 15 THEN 1
            ELSE 0
        END
    ) AS delayed_flights,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN CAST(ARR_DELAY AS REAL) >= 15 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS delay_rate_percent
FROM flights
WHERE CANCELLED = '0.00'
  AND DIVERTED = '0.00'
  AND ARR_DELAY IS NOT NULL
GROUP BY ORIGIN, DEST
HAVING COUNT(*) >= 100
ORDER BY delay_rate_percent DESC
LIMIT 20;


-- 10. Delay Rate by Time of Day
SELECT
    CASE
        WHEN CAST(CRS_DEP_TIME AS REAL) >= 500
             AND CAST(CRS_DEP_TIME AS REAL) < 1200
            THEN 'Morning'
        WHEN CAST(CRS_DEP_TIME AS REAL) >= 1200
             AND CAST(CRS_DEP_TIME AS REAL) < 1700
            THEN 'Afternoon'
        WHEN CAST(CRS_DEP_TIME AS REAL) >= 1700
             AND CAST(CRS_DEP_TIME AS REAL) < 2100
            THEN 'Evening'
        ELSE 'Night'
    END AS time_of_day,

    COUNT(*) AS operated_flights,

    SUM(
        CASE
            WHEN CAST(ARR_DELAY AS REAL) >= 15 THEN 1
            ELSE 0
        END
    ) AS delayed_flights,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN CAST(ARR_DELAY AS REAL) >= 15 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS delay_rate_percent

FROM flights
WHERE CANCELLED = '0.00'
  AND DIVERTED = '0.00'
  AND ARR_DELAY IS NOT NULL

GROUP BY time_of_day
ORDER BY delay_rate_percent DESC;


-- 11. Delay Rate by Day of Week
-- FL_DATE is stored as M/D/YYYY HH:MM:SS AM/PM.
-- Convert it to YYYY-MM-DD before using strftime().

SELECT
    CASE CAST(
        strftime(
            '%w',
            '2025-' ||
            printf(
                '%02d',
                CAST(
                    substr(
                        FL_DATE,
                        1,
                        instr(FL_DATE, '/') - 1
                    ) AS INTEGER
                )
            ) ||
            '-' ||
            printf(
                '%02d',
                CAST(
                    substr(
                        FL_DATE,
                        instr(FL_DATE, '/') + 1,
                        instr(
                            substr(
                                FL_DATE,
                                instr(FL_DATE, '/') + 1
                            ),
                            '/'
                        ) - 1
                    ) AS INTEGER
                )
            )
        ) AS INTEGER
    )
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_of_week,

    COUNT(*) AS operated_flights,

    SUM(
        CASE
            WHEN CAST(ARR_DELAY AS REAL) >= 15 THEN 1
            ELSE 0
        END
    ) AS delayed_flights,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN CAST(ARR_DELAY AS REAL) >= 15 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS delay_rate_percent

FROM flights

WHERE CANCELLED = '0.00'
  AND DIVERTED = '0.00'
  AND ARR_DELAY IS NOT NULL

GROUP BY
    strftime(
        '%w',
        '2025-' ||
        printf(
            '%02d',
            CAST(
                substr(
                    FL_DATE,
                    1,
                    instr(FL_DATE, '/') - 1
                ) AS INTEGER
            )
        ) ||
        '-' ||
        printf(
            '%02d',
            CAST(
                substr(
                    FL_DATE,
                    instr(FL_DATE, '/') + 1,
                    instr(
                        substr(
                            FL_DATE,
                            instr(FL_DATE, '/') + 1
                        ),
                        '/'
                    ) - 1
                ) AS INTEGER
            )
        )
    )

ORDER BY delay_rate_percent DESC;


-- 12. Delay Causes
SELECT
    'Carrier Delay' AS delay_cause,
    ROUND(SUM(CAST(CARRIER_DELAY AS REAL)), 0) AS total_delay_minutes
FROM flights

UNION ALL

SELECT
    'Weather Delay',
    ROUND(SUM(CAST(WEATHER_DELAY AS REAL)), 0)
FROM flights

UNION ALL

SELECT
    'NAS Delay',
    ROUND(SUM(CAST(NAS_DELAY AS REAL)), 0)
FROM flights

UNION ALL

SELECT
    'Security Delay',
    ROUND(SUM(CAST(SECURITY_DELAY AS REAL)), 0)
FROM flights

UNION ALL

SELECT
    'Late Aircraft Delay',
    ROUND(SUM(CAST(LATE_AIRCRAFT_DELAY AS REAL)), 0)
FROM flights

ORDER BY total_delay_minutes DESC;


-- 13. Average Arrival Delay by Airline
SELECT
    OP_UNIQUE_CARRIER AS airline,
    COUNT(*) AS operated_flights,
    ROUND(
        AVG(CAST(ARR_DELAY AS REAL)),
        2
    ) AS avg_arrival_delay_minutes
FROM flights
WHERE CANCELLED = '0.00'
  AND DIVERTED = '0.00'
  AND ARR_DELAY IS NOT NULL
GROUP BY OP_UNIQUE_CARRIER
ORDER BY avg_arrival_delay_minutes DESC;


-- 14. Average Arrival Delay by Airport
SELECT
    ORIGIN AS airport,
    COUNT(*) AS operated_flights,
    ROUND(
        AVG(CAST(ARR_DELAY AS REAL)),
        2
    ) AS avg_arrival_delay_minutes
FROM flights
WHERE CANCELLED = '0.00'
  AND DIVERTED = '0.00'
  AND ARR_DELAY IS NOT NULL
GROUP BY ORIGIN
HAVING COUNT(*) >= 500
ORDER BY avg_arrival_delay_minutes DESC
LIMIT 20;


-- 15. Average Arrival Delay by Route
SELECT
    ORIGIN || ' → ' || DEST AS route,
    COUNT(*) AS operated_flights,
    ROUND(
        AVG(CAST(ARR_DELAY AS REAL)),
        2
    ) AS avg_arrival_delay_minutes
FROM flights
WHERE CANCELLED = '0.00'
  AND DIVERTED = '0.00'
  AND ARR_DELAY IS NOT NULL
GROUP BY ORIGIN, DEST
HAVING COUNT(*) >= 100
ORDER BY avg_arrival_delay_minutes DESC
LIMIT 20;


-- 16. Cancellation Rate by Airline
SELECT
    OP_UNIQUE_CARRIER AS airline,
    COUNT(*) AS total_flights,
    SUM(
        CASE
            WHEN CANCELLED = '1.00' THEN 1
            ELSE 0
        END
    ) AS cancelled_flights,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN CANCELLED = '1.00' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS cancellation_rate_percent
FROM flights
GROUP BY OP_UNIQUE_CARRIER
ORDER BY cancellation_rate_percent DESC;


-- 17. Daily Cancellation Rate
SELECT
    substr(
        FL_DATE,
        1,
        instr(FL_DATE, ' ') - 1
    ) AS flight_date,

    COUNT(*) AS total_flights,

    SUM(
        CASE
            WHEN CANCELLED = '1.00' THEN 1
            ELSE 0
        END
    ) AS cancelled_flights,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN CANCELLED = '1.00' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS cancellation_rate_percent

FROM flights

GROUP BY flight_date

ORDER BY cancellation_rate_percent DESC;


-- 18. Overall Flight Status Summary
SELECT
    COUNT(*) AS total_scheduled_flights,

    SUM(
        CASE
            WHEN CANCELLED = '1.00' THEN 1
            ELSE 0
        END
    ) AS cancelled_flights,

    SUM(
        CASE
            WHEN DIVERTED = '1.00' THEN 1
            ELSE 0
        END
    ) AS diverted_flights,

    SUM(
        CASE
            WHEN CANCELLED = '0.00'
             AND DIVERTED = '0.00'
             AND ARR_DELAY IS NOT NULL
            THEN 1
            ELSE 0
        END
    ) AS operated_flights,

    SUM(
        CASE
            WHEN CANCELLED = '0.00'
             AND DIVERTED = '0.00'
             AND CAST(ARR_DELAY AS REAL) >= 15
            THEN 1
            ELSE 0
        END
    ) AS delayed_flights,

    SUM(
        CASE
            WHEN CANCELLED = '0.00'
             AND DIVERTED = '0.00'
             AND CAST(ARR_DELAY AS REAL) < 15
            THEN 1
            ELSE 0
        END
    ) AS on_time_flights

FROM flights;