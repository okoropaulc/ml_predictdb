-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 20, 2019 at 10:27 PM
-- Server version: 10.1.36-MariaDB
-- PHP Version: 7.2.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `genome`
--

-- --------------------------------------------------------

--
-- Table structure for table `algorithm`
--

CREATE TABLE `algorithm` (
  `algorithm_id` varchar(5) NOT NULL,
  `algorithm_description` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `gene`
--

CREATE TABLE `gene` (
  `gene_id` varchar(15) NOT NULL,
  `gene_name` varchar(10) NOT NULL,
  `gene_type` varchar(50) NOT NULL,
  `chromosome_no` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `job`
--

CREATE TABLE `job` (
  `job_id` int(11) NOT NULL,
  `job_title` varchar(25) NOT NULL,
  `job_description` varchar(100) NOT NULL,
  `job_status` varchar(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `knn_model`
--

CREATE TABLE `knn_model` (
  `gene_id` varchar(15) NOT NULL,
  `population_id` varchar(5) NOT NULL,
  `cross_val_performance` float NOT NULL,
  `neighbors` int(11) NOT NULL,
  `weight` varchar(20) NOT NULL,
  `p` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `population`
--

CREATE TABLE `population` (
  `population_id` varchar(5) NOT NULL,
  `population_description` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `prediction_result`
--

CREATE TABLE `prediction_result` (
  `gene_id` varchar(5) NOT NULL,
  `algorithm_id` varchar(5) NOT NULL,
  `job_id` int(11) NOT NULL,
  `population_id` varchar(5) NOT NULL,
  `predicted_value` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `rf_model`
--

CREATE TABLE `rf_model` (
  `gene_id` varchar(15) NOT NULL,
  `population_id` varchar(5) NOT NULL,
  `cross_val_performance` float NOT NULL,
  `trees` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `svr_model`
--

CREATE TABLE `svr_model` (
  `gene_id` varchar(15) NOT NULL,
  `population_id` varchar(5) NOT NULL,
  `cross_val_performance` float NOT NULL,
  `kernel` varchar(20) NOT NULL,
  `degree` int(11) NOT NULL,
  `c` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(25) NOT NULL,
  `user_type` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `algorithm`
--
ALTER TABLE `algorithm`
  ADD PRIMARY KEY (`algorithm_id`);

--
-- Indexes for table `gene`
--
ALTER TABLE `gene`
  ADD PRIMARY KEY (`gene_id`);

--
-- Indexes for table `job`
--
ALTER TABLE `job`
  ADD PRIMARY KEY (`job_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `knn_model`
--
ALTER TABLE `knn_model`
  ADD KEY `gene_id` (`gene_id`),
  ADD KEY `population_id` (`population_id`);

--
-- Indexes for table `population`
--
ALTER TABLE `population`
  ADD PRIMARY KEY (`population_id`);

--
-- Indexes for table `prediction_result`
--
ALTER TABLE `prediction_result`
  ADD KEY `algorithm_id` (`algorithm_id`),
  ADD KEY `gene_id` (`gene_id`),
  ADD KEY `job_id` (`job_id`),
  ADD KEY `population_id` (`population_id`);

--
-- Indexes for table `rf_model`
--
ALTER TABLE `rf_model`
  ADD KEY `gene_id` (`gene_id`),
  ADD KEY `population_id` (`population_id`);

--
-- Indexes for table `svr_model`
--
ALTER TABLE `svr_model`
  ADD KEY `gene_id` (`gene_id`),
  ADD KEY `population_id` (`population_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `job`
--
ALTER TABLE `job`
  ADD CONSTRAINT `job_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- Constraints for table `knn_model`
--
ALTER TABLE `knn_model`
  ADD CONSTRAINT `knn_model_ibfk_1` FOREIGN KEY (`gene_id`) REFERENCES `gene` (`gene_id`),
  ADD CONSTRAINT `knn_model_ibfk_2` FOREIGN KEY (`population_id`) REFERENCES `population` (`population_id`);

--
-- Constraints for table `prediction_result`
--
ALTER TABLE `prediction_result`
  ADD CONSTRAINT `prediction_result_ibfk_1` FOREIGN KEY (`algorithm_id`) REFERENCES `algorithm` (`algorithm_id`),
  ADD CONSTRAINT `prediction_result_ibfk_2` FOREIGN KEY (`gene_id`) REFERENCES `gene` (`gene_id`),
  ADD CONSTRAINT `prediction_result_ibfk_3` FOREIGN KEY (`job_id`) REFERENCES `job` (`job_id`),
  ADD CONSTRAINT `prediction_result_ibfk_5` FOREIGN KEY (`population_id`) REFERENCES `population` (`population_id`);

--
-- Constraints for table `rf_model`
--
ALTER TABLE `rf_model`
  ADD CONSTRAINT `rf_model_ibfk_1` FOREIGN KEY (`gene_id`) REFERENCES `gene` (`gene_id`),
  ADD CONSTRAINT `rf_model_ibfk_2` FOREIGN KEY (`population_id`) REFERENCES `population` (`population_id`);

--
-- Constraints for table `svr_model`
--
ALTER TABLE `svr_model`
  ADD CONSTRAINT `svr_model_ibfk_1` FOREIGN KEY (`gene_id`) REFERENCES `gene` (`gene_id`),
  ADD CONSTRAINT `svr_model_ibfk_2` FOREIGN KEY (`population_id`) REFERENCES `population` (`population_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
