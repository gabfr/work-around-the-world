class SqlQueries:
    songplay_table_insert = ("""
        SELECT
                md5(events.sessionid || events.start_time) songplay_id,
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id, 
                songs.artist_id, 
                events.sessionid, 
                events.location, 
                events.useragent
                FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
    """)

    user_table_insert = ("""
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """)

    song_table_insert = ("""
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
    """)

    artist_table_insert = ("""
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
        SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
               extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
        FROM songplays
    """)

    recreate_staging_dice_com_jobs_table = ("""
        DROP TABLE IF EXISTS staging_dice_com_jobs;
        CREATE TABLE staging_dice_com_jobs (
            country_code VARCHAR(500),
            date_added DATE SORTKEY,
            job_board VARCHAR(500),
            job_description VARCHAR(65535),
            job_title VARCHAR(500),
            job_type VARCHAR(200),
            location VARCHAR(500),
            organization VARCHAR(500),
            page_url VARCHAR(1000),
            phone_number VARCHAR(500),
            salary VARCHAR(100),
            sector VARCHAR(5000)
        ) DISTSTYLE EVEN;
    """)

    select_companies_from_dice_jobs_staging_table = ("""
        select distinct  
            REPLACE(TRIM(regexp_replace(translate(
                LOWER(organization),
                'áàâãäåāăąèééêëēĕėęěìíîïìĩīĭḩóôõöōŏőùúûüũūŭůäàáâãåæçćĉčöòóôõøüùúûßéèêëýñîìíïş',
                'aaaaaaaaaeeeeeeeeeeiiiiiiiihooooooouuuuuuuuaaaaaaeccccoooooouuuuseeeeyniiiis'
            ), '[^a-z0-9\-]+', ' ')),' ', '-') as id,
            organization as name,
            NULL as remote_url
        from 
            staging_dice_com_jobs
        where 1 not in (select id from companies);
    """)

    select_tags_from_dice_jobs_staging_table = ("""
        with NS AS (
          SELECT 1 as n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL 
          SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL 
          SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL 
          SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20 UNION ALL 
          SELECT 21 UNION ALL SELECT 22 UNION ALL SELECT 23 UNION ALL SELECT 24 UNION ALL SELECT 25 UNION ALL 
          SELECT 26 UNION ALL SELECT 27 UNION ALL SELECT 28 UNION ALL SELECT 29 UNION ALL SELECT 30 UNION ALL 
          SELECT 31 UNION ALL SELECT 32 UNION ALL SELECT 33 UNION ALL SELECT 34 UNION ALL SELECT 35 UNION ALL 
          SELECT 36 UNION ALL SELECT 37 UNION ALL SELECT 38 UNION ALL SELECT 39 UNION ALL SELECT 40 UNION ALL 
          SELECT 41 UNION ALL SELECT 42 UNION ALL SELECT 43 UNION ALL SELECT 44 UNION ALL SELECT 45 UNION ALL 
          SELECT 46 UNION ALL SELECT 47 UNION ALL SELECT 48 UNION ALL SELECT 49 UNION ALL SELECT 50 UNION ALL 
          SELECT 51 UNION ALL SELECT 52 UNION ALL SELECT 53 UNION ALL SELECT 54 UNION ALL SELECT 55 UNION ALL 
          SELECT 56 UNION ALL SELECT 57 UNION ALL SELECT 58 UNION ALL SELECT 59 UNION ALL SELECT 60
        )
        select distinct 
            trim(split_part(sector, ',', NS.n)) as "tag"
        from NS
        inner join staging_dice_com_jobs S ON NS.n <= REGEXP_COUNT(S.sector, ',') + 1
        where LEN("tag") <= 50 and "tag" not in (select "tag" from tags)
    """)

    select_job_vacancies_from_dice_jobs_staging_table = ("""
        select distinct  
            concat(row_number() over (partition by 1), concat('-', 'dice_com')) as id,
            'dice_com' as provider_id,
            page_url as remote_id_on_provider,
            page_url as remote_url,
            location as location,
            null as currency_code,
            REPLACE(TRIM(regexp_replace(translate(
                LOWER(organization),
                'áàâãäåāăąèééêëēĕėęěìíîïìĩīĭḩóôõöōŏőùúûüũūŭůäàáâãåæçćĉčöòóôõøüùúûßéèêëýñîìíïş',
                'aaaaaaaaaeeeeeeeeeeiiiiiiiihooooooouuuuuuuuaaaaaaeccccoooooouuuuseeeeyniiiis'
            ), '[^a-z0-9\-]+', ' ')),' ', '-') as company_id,
            organization as company_name,
            job_title as title,
            job_description as description,
            sector as tags,
            null as salary,
            null as salary_max,
            null as salary_frequency,
            0 as has_relocation_package,
            TO_TIMESTAMP(date_added, 'YYYY-MM-DD') as published_at
        from 
            staging_dice_com_jobs
        where page_url not in (select remote_id_on_provider from job_vacancies where provider_id = 'dice_com')
    """)

    # df.withColumnRenamed('AG_NAMN', 'agency_name')
    # .withColumnRenamed('ANTAL_AKT_PLATSER', 'number_of_acting_sites')
    # .withColumnRenamed('ARBETSDRIFT', 'work_period')
    # .withColumnRenamed('ARBETSTID', 'working_hours')
    # .withColumnRenamed('BESKR_ARBETSDRIFT', 'working_hours_description')
    # .withColumnRenamed('FORSTA_PUBLICERINGSDATUM', 'published_at')
    # .withColumnRenamed('HEMSIDA', 'website')
    # .withColumnRenamed('KOMMUN_KOD', 'community_code')
    # .withColumnRenamed('ORGNR', 'company_number')
    # .withColumnRenamed('PLATSBESKRIVNING', 'job_description')
    # .withColumnRenamed('PLATSNUMMER', 'job_number')
    # .withColumnRenamed('PLATSRUBRIK', 'job_title')
    # .withColumnRenamed('POSTNR', 'zipcode')
    # .withColumnRenamed('POSTORT', 'city')
    # .withColumnRenamed('SISTA_ANSOK_PUBLDATUM', 'expires_at')
    # .withColumnRenamed('TILLTRADE', 'urgency_level_description')
    # .withColumnRenamed('VARAKTIGHET', 'duration')

    recreate_staging_jobtechdev_jobs_table = ("""
        DROP TABLE IF EXISTS staging_jobtechdev_jobs;
        CREATE TABLE staging_jobtechdev_jobs (
            ADRESSLAND VARCHAR(500) DEFAULT NULL,
            AG_NAMN VARCHAR(500),
            ANTAL_AKT_PLATSER INT4,
            ARBETSDRIFT VARCHAR(255),
            ARBETSTID VARCHAR(255),
            BESKR_ARBETSDRIFT VARCHAR(500),
            FORSTA_PUBLICERINGSDATUM DATE SORTKEY,
            HEMSIDA VARCHAR(500),
            KOMMUN_KOD VARCHAR(500),
            ORGNR VARCHAR(500),
            PLATSBESKRIVNING VARCHAR(65535),
            PLATSNUMMER VARCHAR(50),
            PLATSRUBRIK VARCHAR(500),
            POSTNR VARCHAR(8),
            POSTORT VARCHAR(255),
            SISTA_ANSOK_PUBLDATUM DATE, 
            TILLTRADE VARCHAR(500),
            VARAKTIGHET VARCHAR(255),
            YRKE_ID INT8
        ) DISTSTYLE EVEN;
    """)
