-- LIBRARY MANAGEMENT SYSTEM DATABASE

CREATE DATABASE library_management;
USE library_management;

-- TABLES
CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    available_copies INT DEFAULT 0
);

CREATE TABLE members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20)
);

CREATE TABLE borrow_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT,
    book_id INT,
    borrow_date DATE DEFAULT (CURRENT_DATE),
    return_date DATE NULL,

    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- SAMPLE DATA
INSERT INTO books (title, author, category, available_copies)
VALUES
('Python Basics', 'John', 'Programming', 5),
('FastAPI Guide', 'Mark', 'Programming', 3),
('SQL Mastery', 'David', 'Database', 4),
('Data Structures', 'Alice', 'Computer Science', 2);

INSERT INTO members (name, email, phone)
VALUES
('Bharath', 'bharath@gmail.com', '9123531531'),
('Arun', 'arun@gmail.com', '9876543210'),
('Kumar', 'kumar@gmail.com', '8765432109');

INSERT INTO borrow_records (member_id, book_id, borrow_date, return_date)
VALUES
(1,1,'2025-05-01',NULL),
(1,2,'2025-05-02',NULL),
(1,3,'2025-05-03',NULL),
(1,4,'2025-05-04',NULL),
(2,1,'2025-05-05',NULL),
(3,1,'2025-05-06','2025-05-10');

-- LEVEL 4 SQL TASKS
-- 1. Find Most Borrowed Books

SELECT
    b.id,
    b.title,
    COUNT(br.book_id) AS borrow_count
FROM books b
JOIN borrow_records br
ON b.id = br.book_id
GROUP BY b.id, b.title
ORDER BY borrow_count DESC;

-- 2. Members Who Borrowed More Than 3 Books
SELECT
    m.id,
    m.name,
    COUNT(br.book_id) AS total_books_borrowed
FROM members m
JOIN borrow_records br
ON m.id = br.member_id
GROUP BY m.id, m.name
HAVING COUNT(br.book_id) > 3;

-- 3. Count Books By Category
SELECT
    category,
    COUNT(*) AS total_books
FROM books
GROUP BY category;

-- 4. Currently Borrowed Books
-- (Books not yet returned)
SELECT
    br.id,
    b.title,
    m.name,
    br.borrow_date
FROM borrow_records br
JOIN books b
ON br.book_id = b.id
JOIN members m
ON br.member_id = m.id
WHERE br.return_date IS NULL;

-- 5. Total Books Available In Library
SELECT
    SUM(available_copies) AS total_available_books
FROM books;
