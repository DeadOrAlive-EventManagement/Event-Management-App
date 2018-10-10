use SE_Project;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE Customer;
TRUNCATE Vendor;
TRUNCATE Services;
TRUNCATE Events;
TRUNCATE Bookings;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO Customer ( email, first_name, middle_name, last_name, phone_number, pwd) VALUES
('mike@gmail.com', 'Mike', NULL, 'Jordan', '9658741230', 'mike'),
('ashley@gmail.com', 'Ashley', NULL, 'Park', '6758942536', 'ashley');

INSERT INTO Vendor (vendor_name, vendor_location) VALUES
('HKG Caterers', 'Bangalore'),
('Ivy Park Venue', 'Bangalore');

INSERT INTO Services (vendor_id, service_id, service_name, price_per_unit, service_type) VALUES
(1, 1, 'Lunch Food', '30', 'Catering'),
(2, 1, 'Venue for organising small functions', '50', 'Venue');

INSERT INTO Events (event_name, customer_id, budget, num_people, date_event) VALUES
('Birthday', 1, 10000, 20, '2018-10-31'),
('Custom Event', 1, 50000, 50, '2018-11-06');

INSERT INTO Bookings (event_id, vendor_id, customer_id, service_id, booking_status) VALUES
(1, 1, 1, 1, 'Pending'),
(1, 2, 1, 1, 'Accepted'),
(2, 1, 1, 1, 'Pending'),
(2, 2, 1, 1, 'Accepted');

