-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 27, 2021 at 05:09 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flaskproject`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone_num` int(11) NOT NULL,
  `msg` varchar(1000) NOT NULL,
  `date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`id`, `name`, `email`, `phone_num`, `msg`, `date`) VALUES
(1, 'rohit', 'rohit@gmail.com', 999393, 'hello this is pakistan', NULL),
(8, 'ali', 'ali@gmail.com', 2147483647, 'hello this is ali', '2021-06-23 01:26:53'),
(9, 'aslam', 'aslam@gmail.com', 332323, 'Hello this is aslam', '2021-06-23 19:32:14'),
(10, 'gani', 'gani@gmail.com', 393939393, 'Hello gani', '2021-06-23 19:33:24'),
(11, 'koyan', 'koyan@gmail.com', 333333, 'hello koyan', '2021-06-23 19:34:40'),
(12, 'pawan', 'pawan@gmail.com', 3883838, 'Hello this is pawan', '2021-06-23 19:53:45'),
(13, 'daz', 'daz@gmail.com', 345345435, 'hello thsi is daz', '2021-06-23 19:57:02');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `sno` int(11) NOT NULL,
  `title` text NOT NULL,
  `content` text NOT NULL,
  `img_file` varchar(256) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `slug` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`sno`, `title`, `content`, `img_file`, `date`, `slug`) VALUES
(1, 'first post', 'this is my first post and I\'m very excited to create it using flask', 'post-bg.jpg', '2021-06-23 21:12:09', 'first-post'),
(2, 'Second Post 11', 'Hello this is my second post want to just make things dynamic', 'post-bg.jpg', '2021-06-25 00:42:41', 'second-post'),
(3, 'aabb', 'cc', 'dd', '2021-06-25 00:20:34', 'bb'),
(5, 'fourth post', 'Hello this is fourt post', 'img.jpg', '2021-06-26 01:39:48', ''),
(6, 'Fift post', 'This is fifth postfi', '', '2021-06-26 01:40:21', 'fifth-post'),
(7, 'Six post', 'This is six posts', '', '2021-06-26 01:40:48', 'six-post'),
(8, 'Seven Post', 'This is seven post', '', '2021-06-26 01:41:10', 'seven-post');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
