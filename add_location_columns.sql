-- SQL script to add latitude and longitude columns to profiles table
-- Run this in HeidiSQL if the columns don't exist

-- Check if columns exist and add them if they don't
-- For MariaDB/MySQL

ALTER TABLE profiles 
ADD COLUMN IF NOT EXISTS latitude FLOAT NULL,
ADD COLUMN IF NOT EXISTS longitude FLOAT NULL;

-- If your MariaDB version doesn't support IF NOT EXISTS, use this instead:
-- ALTER TABLE profiles ADD COLUMN latitude FLOAT NULL;
-- ALTER TABLE profiles ADD COLUMN longitude FLOAT NULL;

-- Verify the columns were added
-- SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE 
-- FROM INFORMATION_SCHEMA.COLUMNS 
-- WHERE TABLE_SCHEMA = 'xoxo_db' 
--   AND TABLE_NAME = 'profiles' 
--   AND COLUMN_NAME IN ('latitude', 'longitude');

