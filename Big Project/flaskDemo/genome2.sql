-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 28, 2019 at 07:47 PM
-- Server version: 10.4.6-MariaDB
-- PHP Version: 7.3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `genome2`
--

-- --------------------------------------------------------

--
-- Table structure for table `algorithm`
--

CREATE TABLE `algorithm` (
  `algorithm_id` varchar(5) NOT NULL,
  `algorithm_description` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `algorithm`
--

INSERT INTO `algorithm` (`algorithm_id`, `algorithm_description`) VALUES
('EN', 'Elastic Net'),
('KNN', 'K Nearest Neighbor'),
('RF', 'Random Forest'),
('SVR', 'Support Vector Regression');

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

--
-- Dumping data for table `gene`
--

INSERT INTO `gene` (`gene_id`, `gene_name`, `gene_type`, `chromosome_no`) VALUES
('ENSG00000223972', 'DDX11L', 'Pseudogene', 1),
('ENSG00000243485', 'MIR1302', 'lincRNA', 1);

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

--
-- Dumping data for table `knn_model`
--

INSERT INTO `knn_model` (`gene_id`, `population_id`, `cross_val_performance`, `neighbors`, `weight`, `p`) VALUES
('ENSG00000223972', 'AFA', 0.4, 0, '', 0),
('ENSG00000243485', 'HIS', 0.66, 0, '', 0);

-- --------------------------------------------------------

--
-- Table structure for table `population`
--

CREATE TABLE `population` (
  `population_id` varchar(5) NOT NULL,
  `population_description` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `population`
--

INSERT INTO `population` (`population_id`, `population_description`) VALUES
('AFA', 'African American'),
('CAU', 'Caucasian'),
('HIS', 'Hispanic'),
('METS', 'Middle Eastern');

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

--
-- Dumping data for table `rf_model`
--

INSERT INTO `rf_model` (`gene_id`, `population_id`, `cross_val_performance`, `trees`) VALUES
('ENSG00000223972', 'AFA', 0.9, 100),
('ENSG00000223972', 'CAU', 0.5, 50),
('ENSG00000243485', 'CAU', 0.6, 200);

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

--
-- Dumping data for table `svr_model`
--

INSERT INTO `svr_model` (`gene_id`, `population_id`, `cross_val_performance`, `kernel`, `degree`, `c`) VALUES
('ENSG00000223972', 'AFA', 0.3, '', 0, 0),
('ENSG00000243485', 'HIS', 0.42, '', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(60) NOT NULL,
  `user_type` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `first_name`, `last_name`, `email`, `password`, `user_type`) VALUES
(0, NULL, NULL, 'ssiner2@gmail.com', '$2b$12$49wSxH4fT0PLb2CfJpM24.xiJ5ngV.zmtk/EN/ux.18H1exDRQ9Ny', NULL);

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
  ADD PRIMARY KEY (`gene_id`,`population_id`),
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
  ADD PRIMARY KEY (`gene_id`,`algorithm_id`,`job_id`,`population_id`),
  ADD KEY `algorithm_id` (`algorithm_id`),
  ADD KEY `gene_id` (`gene_id`),
  ADD KEY `job_id` (`job_id`),
  ADD KEY `population_id` (`population_id`);

--
-- Indexes for table `rf_model`
--
ALTER TABLE `rf_model`
  ADD PRIMARY KEY (`gene_id`,`population_id`),
  ADD KEY `gene_id` (`gene_id`),
  ADD KEY `population_id` (`population_id`);

--
-- Indexes for table `svr_model`
--
ALTER TABLE `svr_model`
  ADD PRIMARY KEY (`gene_id`,`population_id`),
  ADD KEY `gene_id` (`gene_id`),
  ADD KEY `population_id` (`population_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `job`
--
ALTER TABLE `job`
  ADD CONSTRAINT `job_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

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
