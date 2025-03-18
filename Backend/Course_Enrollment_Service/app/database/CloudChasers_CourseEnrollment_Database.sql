CREATE database CloudComputing_CE;

CREATE TABLE IF NOT EXISTS students
(
    student_id    BIGINT PRIMARY KEY AUTO_INCREMENT,  -- Unique identifier for each student
    first_name    VARCHAR(100) NOT NULL,              -- First name of the student
    last_name     VARCHAR(100) NOT NULL,              -- Last name of the student
    email         VARCHAR(255) NOT NULL UNIQUE,       -- Email of the student (used for login/communication)
    university_id VARCHAR(50) NOT NULL UNIQUE,        -- University-specific identifier (e.g., student roll number)
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- When the student registered
);

CREATE TABLE IF NOT EXISTS courses
(
    course_id    BIGINT PRIMARY KEY AUTO_INCREMENT,  -- Unique identifier for the course
    course_code  VARCHAR(50) NOT NULL UNIQUE,        -- Unique course code (e.g., COMSW4153)
    course_name  VARCHAR(255) NOT NULL,              -- Full name of the course (e.g., Cloud Computing)
    semester     VARCHAR(20) NOT NULL,               -- Semester (e.g., Spring 2024)
    year         INT NOT NULL                       -- Year (e.g., 2024)
);

CREATE TABLE IF NOT EXISTS enrollments
(
    enrollment_id BIGINT PRIMARY KEY AUTO_INCREMENT,  -- Unique identifier for the enrollment record
    student_id    BIGINT NOT NULL,                    -- Reference to the student
    course_id     BIGINT NOT NULL,                    -- Reference to the course
    FOREIGN KEY (student_id) REFERENCES students(student_id), -- Linking to students table
    FOREIGN KEY (course_id) REFERENCES courses(course_id)     -- Linking to courses table
);

#if we want to allow students to create study groups within a course.
CREATE TABLE IF NOT EXISTS study_groups
(
    group_id     BIGINT PRIMARY KEY AUTO_INCREMENT,   -- Unique group ID
    group_name   VARCHAR(255) NOT NULL,               -- Name of the study group
    course_id    BIGINT NOT NULL,                     -- Course the group is for
    created_by   BIGINT NOT NULL,                     -- Student who created the group
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When the group was created
    FOREIGN KEY (course_id) REFERENCES courses(course_id),  -- Course reference
    FOREIGN KEY (created_by) REFERENCES students(student_id) -- Group creator reference
);

CREATE TABLE IF NOT EXISTS study_group_members
(
    group_id    BIGINT NOT NULL,                        -- Study group ID
    student_id  BIGINT NOT NULL,                        -- Student in the group
    joined_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- When the student joined
    FOREIGN KEY (group_id) REFERENCES study_groups(group_id), -- Group reference
    FOREIGN KEY (student_id) REFERENCES students(student_id)  -- Student reference
);

INSERT INTO students (first_name, last_name, email, university_id)
VALUES ('Jeannie', 'Moreno', 'jam2492@barnard.edu', 'jam2492');

INSERT INTO students (first_name, last_name, email, university_id)
VALUES ('Amelie', 'Scheil', 'azs2117@barnard.edu', 'azs2117');

INSERT INTO courses (course_code, course_name, semester, year)
VALUES ('COMSW4153', 'Cloud Computing', 'Fall', 2024);

INSERT INTO courses (course_code, course_name, semester, year)
VALUES ('ECONUN1155', 'PRINCIPLES OF ECONOMICS', 'Fall', 2024);

SELECT student_id FROM students WHERE first_name = 'Jeannie' AND last_name = 'Moreno';
SELECT course_id FROM courses WHERE course_code = 'COMSW4153';

INSERT INTO enrollments (student_id, course_id)
VALUES (1, 1);

SELECT student_id FROM students WHERE first_name = 'Amelie' AND last_name = 'Scheil';
SELECT course_id FROM courses WHERE course_code = 'COMSW4153';

INSERT INTO enrollments (student_id, course_id)
VALUES (2, 1);

USE CloudComputing_CE;
SELECT * FROM courses;

