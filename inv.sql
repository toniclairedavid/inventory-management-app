-- MySQL dump 10.13  Distrib 8.0.29, for macos12 (x86_64)
--
-- Host: localhost    Database: sql_inventory
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT; */
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS; */
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION; */
/*!50503 SET NAMES utf8mb4; */
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE; */
/*!40103 SET TIME_ZONE='+00:00'; */
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0; */
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0; */
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO'; */
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0; */

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client; */
/*!50503 SET character_set_client = utf8mb4; */
CREATE TABLE `customer` (
  `id` INTEGER NOT NULL PRIMARY KEY,
  `name` varchar(100) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime DEFAULT NULL
) ;
/*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;*/
/*!40101 SET character_set_client = @saved_cs_client; */


DROP TABLE IF EXISTS `order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client ;*/
/*!50503 SET character_set_client = utf8mb4 ;*/
CREATE TABLE `order_item` (
  `id` INTEGER NOT NULL PRIMARY KEY,
  `productName` bigint NOT NULL,
  `quantity` smallint NOT NULL DEFAULT '0',
  `customerName` bigint NOT NULL,
  `orderedOn` datetime NOT NULL,
  `receivedOn` datetime DEFAULT NULL,
  `content` text ,
  FOREIGN KEY (`productName`) REFERENCES `product` (`name`)
  FOREIGN KEY (`customerName`) REFERENCES `customer` (`name`)
) ;
/*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci; */
/*!40101 SET character_set_client = @saved_cs_client ; */

--
-- Dumping data for table `order_item`
--

/*LOCK TABLES `order_item` WRITE;
/*!40000 ALTER TABLE `order_item` DISABLE KEYS ; */
/*!40000 ALTER TABLE `order_item` ENABLE KEYS ; */
/*UNLOCK TABLES;*/

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client ;*/
/*!50503 SET character_set_client = utf8mb4 ;*/
CREATE TABLE `product` (
  `id` INTEGER NOT NULL PRIMARY KEY,
  `name` varchar(75) NOT NULL,
  `summary` tinytext ,
  `quantity` smallint NOT NULL DEFAULT '0',
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime DEFAULT NULL
) ;
/*ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  */
/*!40101 SET character_set_client = @saved_cs_client; */

--
-- Dumping data for table `product`
--

/*LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS ;*/
/*!40000 ALTER TABLE `product` ENABLE KEYS ;*/
/*UNLOCK TABLES;*/

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client; */
/*!50503 SET character_set_client = utf8mb4; */
CREATE TABLE `user` (
  `name` varchar(100) PRIMARY KEY NOT NULL,
  `email` varchar(100) NOT NULL
) ;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE ;*/

/*!40101 SET SQL_MODE=@OLD_SQL_MODE ;*/
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS ;*/
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS ;*/
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT ;*/
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS ;*/
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION ;*/
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES ;*/

-- Dump completed on 2022-07-23 10:40:49