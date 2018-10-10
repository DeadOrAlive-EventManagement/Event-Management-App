use SE_Project;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE Customer;
TRUNCATE Vendor;
TRUNCATE Services;
TRUNCATE Events;
TRUNCATE Bookings;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO Customer ( email, first_name, middle_name, last_name, phone_number, pwd) VALUES
('mike@gmail.com', 'Mike', NULL, 'Jordan', '9658741230', 'pbkdf2:sha256:50000$jZzQwZ4G$f304ef7f56c9ff9788f207aed6147d831ed0a397bdcfe33f3c4b110dd9c2eed6'),
('ashley@gmail.com', 'Ashley', NULL, 'Park', '6758942536', 'pbkdf2:sha256:50000$fk1LDC2U$eae508e5b5722ad49e5418885a611c8044f259fa328734c0c9f45d94853117e3');

INSERT INTO Vendor (vendor_name, vendor_location, email, phone_number, pwd) VALUES
('HKG Caterers', 'Bangalore', 'hkg@gmail.com', '8968765009', 'hkg'),
('Ivy Park Venue', 'Bangalore', 'ivy@gmail.com', '7865786987', 'ivy');

INSERT INTO Services (vendor_id, service_id, service_name, price_per_unit, service_type) VALUES
(1, 1, 'Lunch Food', '30', 'Catering'),
(2, 1, 'Venue for organising small functions', '50', 'Venue');

INSERT INTO Events (event_name, customer_id, budget, num_people, date_event) VALUES
('Birthday', 1, 10000, 20, '2018-10-31'),
('Custom Event', 1, 50000, 50, '2018-11-06');

INSERT INTO Bookings (event_id, vendor_id, customer_id, service_id, booking_status) VALUES
(1, 1, 1, 1, FALSE),
(1, 2, 1, 1, TRUE),
(2, 1, 1, 1, FALSE),
(2, 2, 1, 1, TRUE);

