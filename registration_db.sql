-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 28, 2025 at 12:52 PM
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
-- Database: `registration_db`
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
(1, 1, 'samantha', 'tomato ', 12.00, 34.00, 'Annanagar', '2025-03-27 07:20:45'),
(2, 3, 'selvi', 'tomato ', 10.00, 35.00, 'Madurai', '2025-03-27 08:59:46'),
(3, 5, 'muthu', 'tomato ', 11.00, 50.00, 'Chennai', '2025-03-27 09:16:22'),
(4, 6, 'Sarvanan', 'Apple', 100.00, 500.00, 'Palani', '2025-03-28 10:54:27');

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
(12, 2, 3, 'hi i want your product ', '2025-03-27 14:47:44', 1),
(13, 3, 2, 'ok let purchace ', '2025-03-27 14:48:45', 1),
(14, 2, 1, 'aasfas', '2025-03-27 16:28:53', 1),
(15, 2, 1, 'hi i need your product \n', '2025-03-27 16:50:52', 1),
(16, 1, 2, 'fine kindly buy ', '2025-03-27 16:52:04', 1),
(17, 1, 4, 'hi', '2025-03-27 17:17:40', 1),
(18, 4, 1, 'hello', '2025-03-27 17:20:57', 1),
(19, 2, 3, 'hi\n', '2025-03-28 11:00:39', 0),
(20, 2, 1, 'hi\n', '2025-03-28 11:29:54', 1);

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
(1, 'samantha ', 'Madurai', '9244659691', '$2b$12$/meJjNZK0pBc1CdScPOtV.PPXEocvzMFq7no6Gv2/K0YbA54tM4wm', 'farmer'),
(2, 'abc', 'Madurai', '7200099005', '$2b$12$J1ObqetL.ulumacaNCl9P.xTehQ6.vZI9aiHzKTL6qJIpkmJG6DVO', 'market'),
(3, 'selvi', 'Chennai', '8757544313', '$2b$12$3/5oxqsKkEmn26WH7LNFP.pIkZr20tRG5NnyGuw4r89KxWvVpWt8y', 'farmer'),
(4, 'rk store ', 'Theni', '9876543210', '$2b$12$j8iW9o9Vgd/cmTon19qw.OY0pUj4o6h.LZr2XX9IYMXDiILYluWxu', 'market'),
(5, 'muthu', 'Chennai', '1234567877', '$2b$12$R.LJyVqBiutraxvDyDkP8OpAqVUhonTg5WkaETNjIyvdnAXjkX9om', 'farmer'),
(6, 'saravanan', 'Palani', '1234567899', '$2b$12$MhbLgN/n7eg4GN./hNWWGuVoieNjnBIy8gta5D3LUeFXoezh5idw2', 'farmer'),
(7, 'Velavan Sotre', 'Ramnad', '1234567898', '$2b$12$PV6.CbuxB6V4yPRFrUo/ZOylvVZ1Tn6VsdvxXZ.6At2cYLOL.8UJa', 'market');

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
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `recipient_id` (`recipient_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `farmer`
--
ALTER TABLE `farmer`
  ADD CONSTRAINT `farmer_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`recipient_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
