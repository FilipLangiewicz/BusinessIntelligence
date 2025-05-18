-- === DIMENSIONS ===

-- Listing dimension
CREATE TABLE dim_listing (
    listing_id BIGINT PRIMARY KEY,
    host_id BIGINT,
    host_name NVARCHAR(100),
    host_since DATE,
    host_response_time NVARCHAR(50),
    host_response_rate FLOAT,
    host_acceptance_rate FLOAT,
    host_is_superhost BIT,
    host_listings_count INT,
    host_total_listings_count INT,
    neighbourhood_cleansed NVARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    property_type NVARCHAR(100),
    room_type NVARCHAR(100),
    accommodates INT,
    bathrooms FLOAT,
    bedrooms INT,
    beds INT,
    amenities NVARCHAR(MAX),
    price DECIMAL(10,2),
    minimum_nights INT,
    maximum_nights INT,
    minimum_nights_avg_ntm FLOAT,
    maximum_nights_avg_ntm FLOAT,
    has_availability BIT,
    availability_30 INT,
    availability_60 INT,
    availability_90 INT,
    availability_365 INT,
    calendar_last_scraped DATE,
    number_of_reviews INT,
    number_of_reviews_ltm INT,
    number_of_reviews_l30d INT,
    review_scores_rating FLOAT,
    review_scores_accuracy FLOAT,
    review_scores_cleanliness FLOAT,
    review_scores_checkin FLOAT,
    review_scores_communication FLOAT,
    review_scores_location FLOAT,
    review_scores_value FLOAT,
    instant_bookable BIT,
    calculated_host_listings_count INT,
    calculated_host_listings_count_entire_homes INT,
    calculated_host_listings_count_private_rooms INT,
    calculated_host_listings_count_shared_rooms INT,
    reviews_per_month FLOAT,
    scrape_date DATE,
    country NVARCHAR(100),
    region NVARCHAR(100),
    city NVARCHAR(100)
);

-- Date dimension
CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    quarter INT,
    month INT,
    day INT,
    day_of_week NVARCHAR(10),
    is_weekend BIT
);

-- Reviewer dimension
CREATE TABLE dim_reviewer (
    reviewer_id BIGINT PRIMARY KEY,
    reviewer_name NVARCHAR(100)
);

-- === FACT TABLES ===

-- Calendar fact
CREATE TABLE fact_calendar (
    calendar_id INT IDENTITY(1,1) PRIMARY KEY,
    listing_id BIGINT,
    date_id DATE,
    available BIT,
    price DECIMAL(10,2),
    minimum_nights INT,
    maximum_nights INT,
    FOREIGN KEY (listing_id) REFERENCES dim_listing(listing_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- Review fact
CREATE TABLE fact_review (
    review_id BIGINT PRIMARY KEY,
    listing_id BIGINT,
    date_id DATE,
    reviewer_id BIGINT,
    comments NVARCHAR(MAX),
    FOREIGN KEY (listing_id) REFERENCES dim_listing(listing_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (reviewer_id) REFERENCES dim_reviewer(reviewer_id)
);
