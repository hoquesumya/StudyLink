use p1_database;

CREATE TABLE IF NOT EXISTS study_group (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(250) DEFAULT NULL,
    created_by VARCHAR(250) DEFAULT NULL,
    created_at VARCHAR(250) DEFAULT NULL,
    is_recurring BOOLEAN NOT NULL DEFAULT FALSE, -- Indicates if the meeting is recurring
    meeting_date VARCHAR(250) DEFAULT NULL,                       -- Date of the meeting
    recurrence_frequency VARCHAR(50) DEFAULT NULL,       -- Frequency of recurrence (e.g., daily, weekly)
    start_time VARCHAR(250) DEFAULT NULL,                         -- Start time of the meeting
    end_time VARCHAR(250) DEFAULT NULL,                           -- End time of the meeting
    recurrence_end_date VARCHAR(250) DEFAULT NULL,
    course_id VARCHAR(255) DEFAULT NULL,
    members JSON DEFAULT NULL
);
INSERT INTO study_group (
    group_id, group_name, created_by, created_at, is_recurring,
    meeting_date, recurrence_frequency, start_time, end_time,
    recurrence_end_date, course_id, members
) VALUES (
             1,
             'IEORE4150 PROJECT',
             'er2788',
             '2024-04-05T00:58:50Z',
             FALSE,
             '2024-11-05',
             NULL,
             '09:00:00',
             '10:00:00',
             NULL,
             'IEORE4150_001_2024_3 - INTRO-PROBABILITY & STATISTICS',
             '["er2788", "sh1234"]'
         );