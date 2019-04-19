-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: tickets
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alltickets`
--

DROP TABLE IF EXISTS `alltickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alltickets` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `subject` text NOT NULL,
  `body` text NOT NULL,
  `status` int(11) NOT NULL DEFAULT '3',
  `response` text,
  `origin` int(11) NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `ForeignKey` (`origin`),
  CONSTRAINT `alltickets_ibfk_1` FOREIGN KEY (`origin`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alltickets`
--

LOCK TABLES `alltickets` WRITE;
/*!40000 ALTER TABLE `alltickets` DISABLE KEYS */;
INSERT INTO `alltickets` VALUES (1,'network','hello baby are U ok?',0,'hello baby are U ok?',5,'2019-04-16 04:51:21'),(2,'network','Hi dear ellieHow Are You?',1,NULL,5,'2019-04-17 00:51:47'),(3,'el','ellll',0,'nope',5,'2019-04-18 17:47:37'),(4,'ty','ty',1,NULL,1,'2019-04-18 18:02:10'),(5,'tr','tr',0,NULL,5,'2019-04-18 18:03:36'),(6,'nork','e You?',0,NULL,5,'2019-04-18 18:34:41'),(7,'aaaaaa','aaaaa',0,NULL,5,'2019-04-18 18:47:35'),(8,'aaaaaa','aaaaa',0,NULL,5,'2019-04-18 18:47:53'),(9,'wwwww','wwwwwwwwwwwwwwwwwwwwwwwww',0,NULL,5,'2019-04-18 19:03:55'),(10,'fk','fkital',0,'f',5,'2019-04-18 19:04:47'),(11,'peef','pooof',1,'dfg',5,'2019-04-18 19:05:55'),(12,'99999999999999','99999999999',0,NULL,5,'2019-04-18 19:06:28'),(13,'eeee','eeee',0,NULL,5,'2019-04-18 19:07:04'),(14,'dase','gramm',0,NULL,14,'2019-04-18 20:06:48');
/*!40000 ALTER TABLE `alltickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `role` int(11) NOT NULL DEFAULT '0',
  `firstname` text,
  `lastname` text,
  `token` text,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'ellie','ellie',1,NULL,NULL,'12a1fc9658bc7f4e74a2bb4fd2ab1888'),(2,'amirmnoohi','1104',0,NULL,NULL,'d805ff17557f7a164969e07e3a0ad3d4'),(3,'idanrf','110',0,NULL,NULL,'9cfa8a112bc29de5358b623239af0d1a'),(4,'dodooo','11',0,NULL,NULL,'02a0fc9658bc7f4e74a2bb4fd2ab1888'),(5,'al','1',0,NULL,NULL,'dd592f73d78caa4808c7aa43128bd6e6'),(6,'sali','123',0,'saall','saaalll','0722c0321dc2d30f77bc92dcdd796a0b'),(7,'mr','12345',0,'marZ','NoRi','a36527cd04a088b5c48ff110106d37c3'),(8,'ma','1381',0,'m','t','4251f6c8d7180ed6edd98914c838065c'),(9,'q','q',0,'q','q','4c8cfc8293fc5380c91786070d579564'),(10,'test','test',0,'test','test','f4600a4de7275aacaf12c26cd47bb74b'),(11,'t','t',0,'t','t','ccd7eb9ace1c1d6d96781fa1eef9155a'),(12,'xxx','xxx',0,'xxx','xxx','890f773d282ef4a3885b78fbeacd4946'),(13,'zzz','zzz',0,'zzz','zzz','6b0073b359999a255200ad2d0c62bb56'),(14,'mare','1354',0,'ba','fe','233fa3a91398105e2bf63c1313e5ba9f'),(15,'new','new',0,'new','new','84456b299584e31f84fe8a960066d2d4');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-18 20:55:51
