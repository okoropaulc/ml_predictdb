-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 20, 2019 at 12:36 AM
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
-- Database: `genome`
--

-- --------------------------------------------------------

--
-- Table structure for table `algorithm`
--

CREATE TABLE `algorithm` (
  `ID` varchar(3) NOT NULL,
  `description` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `algorithm`
--

INSERT INTO `algorithm` (`ID`, `description`) VALUES
('EN', 'Elastic Net'),
('KNN', 'K Nearest Neighbor'),
('RF', 'Random Forest'),
('SVR', 'Support Vector Regression');

-- --------------------------------------------------------

--
-- Table structure for table `gene`
--

CREATE TABLE `gene` (
  `ID` varchar(15) NOT NULL,
  `chromono` int(2) NOT NULL,
  `name` varchar(10) NOT NULL,
  `type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gene`
--

INSERT INTO `gene` (`ID`, `chromono`, `name`, `type`) VALUES
('ENSG00000223972', 1, 'DDX11L', 'Pseudogene'),
('ENSG00000243485', 1, 'MIR1302', 'lincRNA');

-- --------------------------------------------------------

--
-- Table structure for table `gene_model`
--

CREATE TABLE `gene_model` (
  `geneID` varchar(15) NOT NULL,
  `popID` varchar(5) NOT NULL,
  `algoID` varchar(3) NOT NULL,
  `cross_val` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gene_model`
--

INSERT INTO `gene_model` (`geneID`, `popID`, `algoID`, `cross_val`) VALUES
('ENSG00000223972', 'AFA', 'KNN', 0.9),
('ENSG00000243485', 'CAU', 'RF', 0.3);

-- --------------------------------------------------------

--
-- Table structure for table `population`
--

CREATE TABLE `population` (
  `ID` varchar(5) NOT NULL,
  `description` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `population`
--

INSERT INTO `population` (`ID`, `description`) VALUES
('AFA', 'African American'),
('CAU', 'Caucasian'),
('HIS', 'Hispanic'),
('METS', 'Middle Eastern');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `image_file` varchar(20) NOT NULL DEFAULT 'default.jpg',
  `password` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `image_file`, `password`) VALUES
(11, 'sam', 'ssiner2@gmail.com', 'default.jpg', '$2b$12$rRZUqs8qt6zNcDJCVNJ2eufL8KC6c4bMOq/GlC.4eGk8JNaK7m6C6');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `algorithm`
--
ALTER TABLE `algorithm`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `gene`
--
ALTER TABLE `gene`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `gene_model`
--
ALTER TABLE `gene_model`
  ADD PRIMARY KEY (`geneID`,`popID`,`algoID`);

--
-- Indexes for table `population`
--
ALTER TABLE `population`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `gene_model`
--
ALTER TABLE `gene_model`
  ADD CONSTRAINT `gene_model_ibfk_1` FOREIGN KEY (`algoID`) REFERENCES `algorithm` (`ID`),
  ADD CONSTRAINT `gene_model_ibfk_2` FOREIGN KEY (`geneID`) REFERENCES `gene` (`ID`),
  ADD CONSTRAINT `gene_model_ibfk_3` FOREIGN KEY (`popID`) REFERENCES `population` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
