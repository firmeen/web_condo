CREATE DATABASE IF NOT EXISTS s_residence_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE s_residence_db;

CREATE TABLE IF NOT EXISTS inquiries (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  phone VARCHAR(50) NOT NULL,
  email VARCHAR(255) NULL,
  preferred_building VARCHAR(50) NULL,
  preferred_date DATE NULL,
  preferred_time VARCHAR(50) NULL,
  message TEXT NULL,
  consent BOOLEAN NOT NULL DEFAULT 0,
  status VARCHAR(50) NOT NULL DEFAULT 'new',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_status_created_at (status, created_at)
);

INSERT INTO inquiries (
  full_name, phone, email, preferred_building, preferred_date, preferred_time, message, consent, status
) VALUES (
  'Demo Inquiry',
  '0614518888',
  'demo@example.com',
  'A',
  CURRENT_DATE,
  '14:00',
  'Interested in viewing a room.',
  1,
  'new'
);
