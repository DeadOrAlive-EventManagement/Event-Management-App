use SE_Project;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE Customer;
TRUNCATE Vendor;
TRUNCATE Services;
TRUNCATE Events;
TRUNCATE Bookings;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO Customer ( email, first_name, middle_name, last_name, phone_number, pwd) VALUES
('acb@gmail.com', 'acb', 'ed', 'efg', '9658741230', 'acbedefg'),
('xyz@gmail.com', 'xyz', NULL, 'uvw', '6758942536', 'uvwxyz');

INSERT INTO Vendor ( vendor_name, vendor_location) VALUES
('creepers', 'blore'),
('sleepers', 'MUMBAI');

INSERT INTO Services (vendor_id, service_name, price_per_unit, service_type) VALUES
(1, 'lunch food', '30', 'food'),
(2, 'lights', '50', 'lights');

INSERT INTO Events (event_name, customer_id, budget, num_people, date_event, service_id) VALUES
('birthday', 1, 10000, 50, '2018-10-31', 1);

INSERT INTO Bookings (vendor_id, customer_id, service_id, booking_status) VALUES
(1, 2, 1, 'Pending'),
(2, 1, 2, 'Accepted');

