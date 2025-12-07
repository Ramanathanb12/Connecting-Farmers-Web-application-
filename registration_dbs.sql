-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 14, 2025 at 01:26 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `registration_dbs`
--

-- --------------------------------------------------------

--
-- Table structure for table `farmer`
--

CREATE TABLE `farmer` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `farmer_name` varchar(100) NOT NULL,
  `crops_grown` varchar(100) NOT NULL,
  `rate_per_kg` decimal(10,2) NOT NULL,
  `available_kgs` decimal(10,2) NOT NULL,
  `location` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `farmer`
--

INSERT INTO `farmer` (`id`, `user_id`, `farmer_name`, `crops_grown`, `rate_per_kg`, `available_kgs`, `location`, `created_at`) VALUES
(30, 9, 'Farmer 1', 'Wheat', 467.30, 120.00, 'Madurai', '2025-04-14 10:30:55'),
(31, 10, 'Farmer2', 'Wheat', 300.80, 120.00, 'Namakal ', '2025-04-14 10:33:04'),
(32, 11, 'Farmer3', 'Wheat', 262.16, 120.00, 'Theni ', '2025-04-14 10:34:04'),
(34, 13, 'Farmer4', 'Groundnuts', 428.15, 50.00, 'Ramnad ', '2025-04-14 10:43:42'),
(37, 14, 'Farmer5', 'Rice', 809.58, 120.00, 'Dindugal', '2025-04-14 10:50:48'),
(38, 15, 'Farmer6', 'Rice', 526.77, 120.00, 'Viruthunagar', '2025-04-14 10:52:35');

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `recipient_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime NOT NULL,
  `is_read` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `sender_id`, `recipient_id`, `message`, `timestamp`, `is_read`) VALUES
(0, 12, 9, 'hlo sir ', '2025-04-14 16:52:25', 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('farmer','market') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `location`, `phone`, `password`, `role`) VALUES
(9, 'Farmer1', 'Madurai', '123456789', '$2b$12$9xefCYrwIsiyrRSrJoSise00QYudUpvecB4afLGd10LpbhVmZivL.', 'farmer'),
(10, 'Farmer2', 'Namakal ', '1234567898', '$2b$12$dmgsFdE8TODdRqIyyBw9yen9ill8LPDTCYjlkN8HGbhRfoZ1xH9hC', 'farmer'),
(11, 'Farmer3', 'Theni ', '1234567899', '$2b$12$36ChmC8SEe1V8nF7l57U7OhIUxb1zqghezkk9g2De5kqtU6TH/S5O', 'farmer'),
(12, 'Market 1', 'Chennai', '987654321', '$2b$12$/Mnxhyk0S52y5V/G3/KPZeVJUF4gkvC84jvk/wQnkeYw7SBMB2WS2', 'market'),
(13, 'Farmer4', 'Ramnad ', '1234567890', '$2b$12$RxZozYzgPpJv2CRm7AgkKOuGfJkQBqmjtT1JAr3prJzXVFhUn3XzO', 'farmer'),
(14, 'Farmer5', 'Dindugal', '1234567891', '$2b$12$PSzColJhcLxAX.yQXVqeneNQJJ/w5Ttif7n8da2pwFDeaZCNxANX.', 'farmer'),
(15, 'Farmer6', 'Viruthunagar', '1234567892', '$2b$12$SZBEkxkNb9rgiVD7nPmptuoDMrh2Uus93NQ9uwP.KjCGefChgsn7.', 'farmer'),
(16, 'Market 2', 'Banglorre', '9876543210', '$2b$12$isc69FoQCePft13aalIEL.wDS4lH3MycIfU0VPab6QN/e3/r.7SXK', 'market');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `farmer`
--
ALTER TABLE `farmer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `farmer`
--
ALTER TABLE `farmer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `farmer`
--
ALTER TABLE `farmer`
  ADD CONSTRAINT `farmer_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
