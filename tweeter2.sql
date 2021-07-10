-- MySQL dump 10.13  Distrib 8.0.23, for osx10.15 (x86_64)
--
-- Host: localhost    Database: tweeter2
-- ------------------------------------------------------
-- Server version	5.5.5-10.5.9-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment_likes`
--

DROP TABLE IF EXISTS `comment_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment_likes` (
  `comment_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_likes_UN` (`comment_id`,`user_id`),
  KEY `comment_likes_FK_1` (`user_id`),
  CONSTRAINT `comment_likes_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_likes_FK_2` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_likes`
--

LOCK TABLES `comment_likes` WRITE;
/*!40000 ALTER TABLE `comment_likes` DISABLE KEYS */;
INSERT INTO `comment_likes` VALUES (13,52,8),(15,56,9),(16,59,10);
/*!40000 ALTER TABLE `comment_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `tweet_id` int(10) unsigned NOT NULL,
  `content` varchar(280) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT curtime(),
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `comments_FK` (`user_id`),
  KEY `comments_FK_1` (`tweet_id`),
  CONSTRAINT `comments_FK_2` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comments_FK_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (17,'Dude',49,'2021-06-29 20:54:17',9),(17,'Meow',49,'2021-06-29 20:55:20',10),(21,'Love this, pear',52,'2021-07-02 19:21:29',13),(21,'This looks great, pear',52,'2021-07-02 19:23:34',14),(17,'5',56,'2021-07-02 19:58:44',15),(24,'comment',59,'2021-07-03 14:44:50',16),(21,'You truly are',59,'2021-07-06 16:37:13',17);
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follows`
--

DROP TABLE IF EXISTS `follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `follows` (
  `user_id` int(10) unsigned NOT NULL,
  `follow_user_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `follows_UN` (`user_id`,`follow_user_id`),
  KEY `follows_FK_1` (`follow_user_id`),
  CONSTRAINT `follows_FK_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follows_FK_3` FOREIGN KEY (`follow_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follows_CHECK` CHECK (`user_id` <> `follow_user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follows`
--

LOCK TABLES `follows` WRITE;
/*!40000 ALTER TABLE `follows` DISABLE KEYS */;
INSERT INTO `follows` VALUES (52,49,18),(56,41,20),(56,49,22),(59,41,24),(59,42,25),(59,49,23);
/*!40000 ALTER TABLE `follows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `user_id` int(10) unsigned NOT NULL,
  `token` varchar(100) NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login_UN` (`token`),
  KEY `login_FK` (`user_id`),
  CONSTRAINT `login_FK_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (41,'JQKyeITzwgiPahPZU7OX16j3jVU',53),(42,'imdf_m9RDTSZLiJizDYKYmeHHLQ',54),(43,'p3I87tRwob3uJ6NRqBy8LT6_6ok',55),(44,'eofQRiYf8eIQ4acgDwvH03hK9oE',56),(45,'74vT0_tdvJHi9MyC29-fmg_VaPg',57),(44,'CLhQvgkAXbgPzzb7lMGpOAMhxXc',58),(44,'KMRLUwPF79EYlYydPyeLODrse1o',59),(48,'N-BRQwqxhdRlX41hduL6oH7vvF0',64),(49,'gWlJouD0_aykFXiQeTiZij2mDMI',77),(49,'5C_IG-yRImrj-PIY_ouzJrc68Tc',79),(49,'S1ZUYX-A4fHdmIKW-SIsnf7Myvg',93),(58,'R2W6hCvXKzZaaOgtFQNFAH1faSg',102),(59,'PhJoPX_HnSzMHM8-xDXUcLezUeo',103),(58,'DHxv5OmxhkInVXHGTrq52B9T5Lw',104),(59,'GyJdILmSP7656YPomIfa7omKM6I',107),(60,'ehSNixfPo2k2GLfMK3vVzG3Zjko',109),(59,'WBJr5aOsZVIJng-XmE1qP5g6t5M',110),(59,'g_Ui_uR9c4Vy_ObfiZnw1OVJQnk',111);
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet_likes`
--

DROP TABLE IF EXISTS `tweet_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tweet_likes` (
  `user_id` int(10) unsigned NOT NULL,
  `tweet_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tweet_likes_UN` (`user_id`,`tweet_id`),
  KEY `likes_FK` (`tweet_id`),
  CONSTRAINT `tweet_likes_FK` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tweet_likes_FK_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet_likes`
--

LOCK TABLES `tweet_likes` WRITE;
/*!40000 ALTER TABLE `tweet_likes` DISABLE KEYS */;
INSERT INTO `tweet_likes` VALUES (49,17,30),(52,21,33),(56,17,37),(56,20,35),(56,21,34),(59,17,39),(59,21,40),(59,24,38);
/*!40000 ALTER TABLE `tweet_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweets`
--

DROP TABLE IF EXISTS `tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tweets` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `content` varchar(280) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT curtime(),
  `tweet_image` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tweets_FK` (`user_id`),
  CONSTRAINT `tweets_FK_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweets`
--

LOCK TABLES `tweets` WRITE;
/*!40000 ALTER TABLE `tweets` DISABLE KEYS */;
INSERT INTO `tweets` VALUES (15,42,'This is a tweet','2021-06-29 16:43:26',NULL),(16,41,'hi','2021-06-29 16:43:26',NULL),(17,41,'Hello','2021-06-29 16:43:26',NULL),(20,49,'I am a pear','2021-06-29 20:56:41',NULL),(21,49,'I am a pear dude','2021-06-30 15:52:53',NULL),(24,59,'Felt cute, might delete later','2021-07-03 13:00:11','https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Coffee_beans2.jpg/220px-Coffee_beans2.jpg'),(27,59,'this is a thursday type of day','2021-07-08 17:03:34',NULL);
/*!40000 ALTER TABLE `tweets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(30) NOT NULL,
  `email` varchar(255) NOT NULL,
  `bio` varchar(300) DEFAULT NULL,
  `birthdate` date NOT NULL,
  `image_url` text DEFAULT NULL,
  `banner_url` text DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `password` varchar(150) NOT NULL,
  `joined_on` date NOT NULL DEFAULT curtime(),
  `salt` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_UN` (`username`),
  UNIQUE KEY `users_UN_email` (`email`),
  CONSTRAINT `users_CHECK` CHECK (`username` <> `password`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('five','five@mail.com','this is the fifth bio','2000-09-12','image','bannerUrl',41,'9776b3524cd234e97dd042b9e0e2a1d7eeac359abef027d71cd9231ea4eba879a1430a1e7d143d88d4b6b8f311c5669c15e931b685bc9b370fc8293f071f07de','2021-06-26','JFnJ3ZFiMo'),('four','four@mail.com','this is the fourth bio','2000-09-12','image','bannerUrl',42,'9c3ea73f73abc2e7717ed8e04e26290b2a2084a822dc234e576a35524b57243b20d498bd0234bbcb497e6e1172c0aba6c9d2abedf6e9f965222e43ec859ff9fa','2021-06-26','8AgDieuEva'),('three','three@mail.com','this is the third bio','2000-09-12','image','bannerUrl',43,'0bf339aa117193cfb86350279012ef53c54efc248505dac3da6482578ba2634962913498c24973e7a5a613d25c4813308d79073ca399c4646e0e957287be02a3','2021-06-26','yoX9Mc9LjQ'),('two','two@mail.com','this is the second bio','2000-09-12','image','bannerUrl',44,'380f33031a91a911599023ff2eef1b05dc5ecaa2e22d18608c6a179cba652a256cbbc0436715abfc07f2456623f4941b79039f62a4ad8312d5415b1c81a44af6','2021-06-26','cPTPWtQHkP'),('one','one@mail.com','this is the first bio','2000-09-12','image','bannerUrl',45,'83ce80a55e8635d6d3128d6875fb56fd719aea962072d2be6c9805c03d143528b05617bb27f74c942cbf82076a36cfcd8e5e33c465ae9e99fee7c7c0da3b89e7','2021-06-26','ScbEYfUyZ3'),('apple','apple@mail.com','apple','2004-09-29','data:image/jpeg;base64,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',NULL,48,'0fe75c6f637ed905aa1f5bf51f1d0eb9458506c6250bd2c2510a1cf557546e52fe05f27f6c68d99ffce1989988ffffe165f67d21a7841ceb6a3f0659065f24e9','2021-06-29','5UTXn0A9Gi'),('the_pear','pear@mail.com','THIS IS BIO','2013-05-29',NULL,NULL,49,'c1e094b79fb9abac536b74fdc7e29242f566740cb1bc1d98a85183b9c20b574bc6076ad1b013c87e79d614e0ce5d805ef02c7f2067dafe84f812466790441d3e','2021-06-29','BtTXWJR4Hl'),('noodle','noodle@mail.com','the best noodle you have ever met','2006-09-02','https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Mama_instant_noodle_block.jpg/1200px-Mama_instant_noodle_block.jpg',NULL,52,'18ad63e63653a022d3c902b46025e8df5feaf63401c5f6e0b6b9b73c301dbf7274ecb566ae1e864dee9bfc2e1b2fd911d2a11d73d9de484a9be4d773a0dec89b','2021-07-02','zSO53d41rH'),('tester','tester@mail.com','test','2021-07-02',NULL,NULL,55,'d23a7b4bb2a19fb356e4ef345129cf12bc0f07f9ba3629e37fcd5550a9a61d62a50b8ab045be7412e90ae27eb0c497da7273e6eb6164dd9294f27659dc7c7de9','2021-07-02','PvdGaNMfrv'),('test','test@test.com','bio','2021-01-04',NULL,NULL,56,'67a3fb10bd8a0c9b036fdd925964beb05b5fa2cc1acdaba420070c0ce15251be8758eef0e8a8299a98408cd16a03c22822d2ebfcd5304c179684a7b53a3f19bf','2021-07-02','1nV5yyJOzp'),('toast','toast@mail.com','this is the toasts bio','2000-09-12','https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Toast-2.jpg/200px-Toast-2.jpg','data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUVFRgSFhUVEhgYEhISEhkYEhgYEhISGBgZGRgUGBgcIS4lHB4rHxgYJjgmKy8xNTU1GiQ7QDs0Py40NTEBDAwMEA8QHhISHzYrJSs0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NP/AABEIALcBEwMBIgACEQEDEQH/xAAbAAAABwEAAAAAAAAAAAAAAAAAAQIDBAUGB//EADgQAAIBAgUDAgQDBwQDAQAAAAECAAMRBAUSITEGQVFhcRMigZEUMqFCUmKxwdHwByPh8RUWclP/xAAaAQACAwEBAAAAAAAAAAAAAAABAgMEBQAG/8QALREAAgIBBAEDAwQBBQAAAAAAAAECEQMEEiExQRMiUTJhgQUUcaGRM0JisfD/2gAMAwEAAhEDEQA/AMOqxxVgURaiUS8BVjgWBRHFEAQBYYWKURYEUIkLDCxYEMLOOEaYemOWjVSuq8mcABWJKyLUzNBItTOF7RlFgtFiyxlxKupnEiPmjGOoSA2i7a0ZZx5lG+OYxBxDHzGWNibkXbVV8xpsQspi7esHzesPpg3fYtmxSxs4sSs0N6wfDbxDsXydb+CecYIRxcgfDMAQw7EC5fBNOKiTipEKGFoMO1Hc/BL/ABUH4mQ9EFp21HW/gl/iYPxEiWgtO2oG5/BL+PD+NIdoJ21HbvsS/jRQrSFeDXO2nbkTvjCNtUBkTVD1ztp25DtoI1rgh2sFxNYqxarH0oyTSwt5VbJyGqxxVl1hsrDcmXOFyOn33iOaCZFUMdTDseFJ+k3dLLaK9lkpKdFf3RF3nWYJMvqH9gxf/jn/AHbTfo9L0mf6vz+jQpFVsWIsLczk23SBuMDnOY6LqOZl62NZjzEYzEl2LHuZGBl+GNJcleWRt8EhW8mL1CR7wwIzicptEkMvpD1rI2mKCHxFpDrJLwh/WsL4wja4Zjwp+0d/8dU/dP2g9q7YU8j6X9BfHEH4geIiphGXlSPpEth2G5U/aFKIHPIvH9Dv4n0hnF+kilTHaGHZjYC85xiuWcp5G6Qs4n0iDiDL/AdJVqltrXmgo/6em253leeqwQ4snWHM+3Rz74xg+KZ0Or/p+NOzbyhxfRtZeNxDHVYZeRZYMq6dmZLmJ1mWtXIKoF9JMr6uFdTZgRLEZwl0yGWPJHtMa1mF8QxQpGT8Fk1SpwIZShFW2CMJydRRXajBea7DdHsd22llhukUH5jeVpazFEnjo8j7MCtNjwCfpFCg5/ZP2nVKGRUkGygwjl6C4CL9pC/1BeESrQryzlT02XkERu86HmmXIyn5Rt4ExmMwQUnTxLOHURyEObSyhynZXQR3RBJ7RV2s3yKZIp6pbphBJCYVZmOZo7CspVag4/lJC4it+8ftLRMMskrRWK5HbSjtVPLNFLRfyZfrTWVmfZrTwyFjbUR8o7wJtukdSM7n2amgunUdRHnic9xuLao2piT7mPZpj2rMXY8naQJo4se1W+ynlnudLoTDAghgSYhF01lhh8IDICzR9M5a9ZhYGwMhzy2xbstaaEZSposcm6TNWxPE1+F6NooNxcy/y3BimgX0kxhcTAy6vJJ98GioxjwkVGH6doL+wJOOUUv3F+0eoI17mSllZzk+2FtlNX6foublB9pFx3TtBltoA2mgcyiz/NVpKSTvY2kkJzbSTDHlnPswyyijlbjmNUPhowK2O4lNmmOZ3LX5JjeAdmcDm5E2lils9zE9SCntSOy5FiFdARbiXJlF09hCiA9yBLwN5mHkrdwPP6uBiqbyI9PVtJ9S0jBd9oqYEQ2wSja0pc2yBKgvpAPtNO7AC/eQK+J2JK2k2Ock7Q6tnKMxy00Kmk8X2ms6cqLa20pOrsWrOLciTOkfmN/E0ctywqTBBRjJxRtWQASObR+oTaR3O1pnJjBM8hYm97g7+JKc2kWrTN9XMeISOy35EqMxy9SDwJdVK6qdN95RZxmKr3uZYxbnL2iTquTJ1qBDEeDBEVsTck+TBNdKRn3A68kfQSOrR9HmYWSSix9EkZHh4nGrTQ1HIAAv/wAQCsTm2YphkNRz2+UdyZx/PM2fEOXY7X+UeBJPUueviahYmyg2QdreZRGaODDtVvsp5st8ITChw1EslYCiOWgUS2yPCK7jWbKOYk5qKbZNixOckkPdPdPVMQwsCFvuZ2DIciTDoFA37mQ8kr4ekoVCtv1l7Tx6EXBnntVqZ5ZVVI044vTVJfkkfCjFRrc7SLXzdFvcynxXUlIjc8GVowk/A8YyZo0a8W9QKLzD4jramuyAmZnM+s6z3CnSJPDR5ZvqguKX1M6Dmuf06QNyCZy/P85au5N9r7SpxGNZjdiT9ZGapNTT6OOPl8sjnmilUQcm3k2nQOkshpqRUcgnm3ic/wAPfUD6zTYXFPwpY+0fVqTjti6E022Tcn34OtrWQCwItI7t82oHt52nPqFPFvcJrPnmLqUsao3DW95k/t+fqRb2L5OgviFC3JH3jDYtFFywH1nN8RmFdRZtY+8i4nMn02ueI8dG35Ee2PDOgY7qOig3YH2mRzrq3WCqDbzMjXrknc3kVqk0MOhhHl8kM86j0PvUNRwCeTuZ0DIBTpKACPU+s5xgzdxLM12GwJH1kupwuaUE6F0uRNOT7bOnV8clvzC/vGzi0A3YTm34lz3Jk1TXIsFc34+U7yj+zryWt8TRY7OwptcW7Svq9S2FhKt8jxLDWVIFtrnc/SVeJw7r+ZWW3NwZYx6fE+LshlmkvBNxedMxuNpUV6xbcm8Q7Rt2l6GKMekZ+bPKXAV4IiCS0VrOxo8kI0g05MoiYzNmiT8QKCzGwAuSewnOOquoDXfQhIpqbD+I+TJXVnUGsmjTPyA2Yj9s+PaZAmXdPhr3SKWfL/tQRMSYCY5RpFjYAk+kt9FNJt0hsCX2V9MYiuNaoQvk7TU9IdHDarWG97qvp6zo9CkqjSAFA4AG0zNT+oKD2w/yXselS5n/AIOc4L/TgkXepbbgCOjoB1Py1Lj15nRvYRarbeZz12Z9stRhGLtIzmS9LJRs7Es1u/EvGwakWA079pIQ6twQRHAPErTnKTtsZybILZej/mQbcSmzbpWlUU6fkPYji81O0ouoc6TDrdrnxbzHxOe5bWdGUm6RyXPspOGbQzAsdwB4lIWvLXqDM2xD6rX3svn2mg6W6SLAVKg35APabvqrFjUsnZHKMpz2rpdso8o6brVyPlIU9zNzl3QtFANQLn14vNfgcEqKFAAtsNpNItMrNrck+nS+wyUI9L8mcHSWHtb4aj+cnYfJqKABUUW9N5YubjxCLi1u8rPLJrljWNJRReABeIeircjiNVKus2R1IBs9je3pJd7CK7CV2Iy2m4IZAfpML1bkCIpdTYje3a03mPraEJv67nvOW9SZy7tpJ29+0uaNTc1TG7i2+jKPUisPg6lQ2VS3sJtOlejS5WvWA0H5lXufBM31HLkT8qKtuLAAzRz6+GJ7Yq2UY6Zz5m/wjleB6TxV9Wi1vJAMvsJ0a2ofEYbi5C9vQmbqoNNydv7Rq479+b+JQnrss/sW4YowVJFVgslo07aVBPki8tVpjwPSGdKje3pCQ33/AE7iVZTlJ22SWMYki1+PpKTE0LhtW4IIAIFpd4hiLBQDv3Yg/TbeVePptyLEjcjzJcZxgs8ypEGpDYjkdj7TPTY9UnYHb2HMyQE3dNKTh7mZerhFSW1DemCOWgk9lXadcpUpnOqs+0g4emd+KjDt/APWTeqM8FBfhIf9xhuf/wA1Pf38Tnbvf+Z8k+ZRwYb90i/mzUqQlmiCYTGCXkig3YFE3/ROQVFPxHSwIBW/JHtIXQeBpsxqOoYq3yk/lH08zqeHU22At/SZeu1TV44r+TR0uDalN9vodw9O3a0lKJGRQVKC4FrXHI9pJQW2uTMVllhsneINNtRJY6bW09veOM3+dokhr7nY+NoGwIFEKg0gW34/rHLte1hptzfe/tDUeIlnHt5g7OEYisFBJ2AE5R1pmwqOUBuBNb1Zj1RHIJLEW/MSB6AdpzDBWqV1Vz8rONXHHjeaehwrnI/A/wBEfu+DUdDdOfGIruNQDWVTwfUzqGGwwRbWtbiRcqp00UKgAFhxaSxWAYi/YWFxYfSVtRnllm7E64Q67gDfiBmFhfufqY27i4Nxbz3iK7m62F7/AGt5lZoCQeIv47/YRBAsP2r8+LRGIRmGxUHuG3FvpxFJxY/1h8DITSwypcKqqCbkKABYQqjW82+n8447DvY9vtKXOcxRV2bf/O8KTk6GirZnOsM4FtCnzf3nPA4LjVuNQ1eovvJ2eYnVUbwDYSnZrEH1BnoNLgUIfyQ6nKl7V0juWXampIVK076Sbrf5O4AvsbSdV473lJ07igaKXcXKCxubt55lo1YkXXz73mHki1NonoDnULFebfWIdV7jc+v6w0f13837ekUiL37nm+5irgJCxFBWYagbKbgl7b9haOjzttx7SUVUeviQ8W9h2v2F7e8ZO+DrG6uJAIX5iWGxsdPtfgGQ6yaRu25vzxYn9Y7RrG5BFu6/Nfa36Qma/OxO+5F7+BHXB1GI6ppixIFgPO1/YTIgzedTUVKne2x+hPMwE29I7xmfrOJJjl4IUEtFOx3EV2dizEszEsxPJJkYmGTEwpULKVsF4FEcpUWY2VSx8AEn9JoMB0hiahF1CXG2oj+XaLPJGC9zoaGKU/pQOmc5/DndQw1X9R7Tf4Lq2ky+NhtKPBf6esQC9a3nSoIHobm/6SW3QqKDau1+FJC6Qf4rc/SZWd6bJK75NbDujFRkui6bqumtgBzzvsPWTv8A2GmRfWF8G1/0nPsR0/WFQUqZFba+tflVSOQ3Nt5ZVemMQRsy7bftbn7SvLBiVe4l4b6NkOoaIAu6sTbgcn27SNX6ww697/3mAxmR4pD+Ut22N/pKCqxBINwb2IPIMkx6LHLlSs6W2PaOnYjrhB+Ue/Mz+N6xqNfTZQST/wAzHGpDpqzkKoLMTZVUEsT4AEsw0WOPLF9VLpErH5i9QksxP12lSaliD6zovSnQ5f8A3cSrAbhaRDKT/ExFiB6D/ia/B9HYOmSVw6Em19WqoBbxrJt9J0tZhw+1c/wV8qlOuaOdZX1TVpqEBB4FzzYcCWdDq2pyd7m58H0m/fJsO3y/h6BHYfDX+g24jVTIaDEs1Kncm5+TVt4/lKM8+GTvaWFL5KDB9TKV1MB2Iv2+0lf+10dQY3JsQLDm/PeP5j03QKELT33to+Ui4/X2mEHSuKeoyKhCrvqf5Fta9vffgQQx4clu6GUo1bRrH60ob7H697dtpDxPXK3IUHjm36TM5h0fiqSayFcDkIxLKPJBA/SZwsRfzwfIlvHpML5i7Fc0vBqsb1dUbj23Mo8RmtR73Y787ytLxJaW4aeEekRyzsKu3eR13MlUsLUqnTTR3sd9KE2PrbiW2E6WxBKh1+ED+0w2HuBJ5ZIQXuaRScZ5Z8Lgt+ls+SktmVbgBQ2kareCfE1+HzSm4B1gDiw8TLYbompYkVQwBt8iXB82JIvItXJMQrFVpO4XhlBF/p5mVlhhyybjL/35NOD9q3Lk3FTH4cHXZQTa507m3G8jr1CjNoBvM03T+NOkFbBu+oEJ/wDVuIY6bxFElyVY2AUKST7m8i9DGlzLk7cr4Rra+OUrswW4PexBkJsbZTqYEjvaxI41WP8AKZHEVKqfmDAg8FTKuvmDm+8aGkb6YNyXZt6uaILfNYbccn3MrMZ1Gq7Kb+PNpjXxTHuY0zS3DRRXbI5Z4ros8fmrPf8AwyiPJ94/eMNyfeXccFFUihqJuVNioIII5ANzT5L00XKtU4JHyg228lv6CVuRZe1WoDpJAN+O86dgKOkBRYW52Bb7ylrNS8fti+S7pdOpLfJfwhWW5XTorZFVbcNpux8m5lmiH6eADc+pMbXVsLyQh28n6zEnNydtl/oeCDbYLY322HFosUltcjnf0HvGVYqL3sfJ32+sXRYNvqFS/wDECP0kdMA+mw2X6cD3jwU88f52jC3uTcAeOf8AqPqfMVsVjVWmp7C/qP8AN5znrnKzqFVRTUC4b50V2vwTYDxYXJnRMTUtewBJG3tOY9bY7U+jbg6ue9v7D7S9od3qKjmrg7MkHuQBySAB5JnaOkMjTD0wVUa2RC78sTbdRcbD0mJ6D6bDsK7g/KwZOLG3e3mdYVABbiT6/UL/AE4fkghFpXLti2NtzEs4C3PiNvUv9OY1VYsLDa4tczJslSBSqhhqHB258SShNuL/AKSFluCWiukFjdidySAT2F+BJrC58ePedxfBzCYHsP7fWE6A2B47/wBooJ3ufbtAy3nAGK6CxGw8eswfWeR0fhviLaGVTp02sx5u1vr95vqhHe0y3VVFWoOCdPynv2t4lrTTcciphq1Rx2mGchVBLE2AA3P0m7yHoi6/ExAN7BggYAH0bvM70xXFOsGsOwBtxvOu4D57G9xpB4295pa7UTh7Ycfciw4Vt3S5/wChrLcBSRCqU0UG2yjvxckyf8IGwP8A2faOlOPAgJHN795jSk27ZPYQTa3b22hIBwAABtDLX49/eJpbjfm5i1ZwdRdvH+cSC63O1j6nx4kjEm4t/hkXXp2C28xo34ORFxVDVcWFiCDt95msy6aRhqNkNh+Uf0mqQ3Bud9x7SNV+XYDUbi/pLGPJKD9rG74ZyvNcsag1iQw7Ef2lYXnTOocMrqdlvbv/AEnM61GzEes29Nm9SPPZQ1OPZTj0xDP4hKIoLFWlmyntb7E2hw7QQD0dFyPL/hKBp5Av/YmaDDof7bkfW0Zw4Ekb7e++887km5ybZspUqQ6im+xvv/lpIRwOTv3jCf8AUWGBNjvImgkl1UrYi4O2/cQsHh1prpQaVv5J9Tz2iRUB+lo4ri31i+KFFBGLFtfykAABbH7x/WF2vxzIz4nSOx/kJQZpny0rlmDN2AnRxym6QUmyyzjMURSxNtj3teYjK8B+Mrs7AhAfoT2Er8RjamMqhbkC/HZROh5LgFpKqKdlHzeSfMutftof8n/QbVUi6wKJTRVVQoAAUCSC5O2w9e8aHH8opD43PeZsm2yJgqM1rCO06ZA5v7iGBteEX8QHWOrCYC9/8ESj/SKvAwB3iKjMPETUbsIxia2mMl8HJDGJrE7WtMB1lmKgaQfm/Kd+BNFnudLTUtcegnKcyxhqOWPc3mpotO3Lc+jsklCNisvazj1Ina8lf/aXv8o7WnCsJUs6nwQZ2Hpis7orE7W2Em/UY9MTBLfjf2ZoX+a4IIjFQEWUbCSy0h4l+9uOJj9skQ8l7EHt3jbVBwPrG8PXLCxjdZbcfWGuRq5FvfVftGK1QfmO3iCvV0rcb7bmRgyvZuw7esZRGSFoLn0iHBUGw3O5igbRiu/zXvtGXYSqzBLqSdjYznGPSzn3m/zrFgA7zn+NqAsT6zW0KfJX1VbORgQGJBgmgZ9gvBCghFs6hhsep4Ikr8SxtYrbe/8ASc2pZgy8GSlzlx3mVLRO+DUjmizoi1vJ2ia+PVBfUP6zADOn8mN1szZhzFWjlfIXlijYN1Dbcflvz39oxW6vAFgJiPxDXIubHe0bqMZYWihfIn7hV0aDH9U1HFgdI/WUNbEsxuSSfWMGILS1DDGP0orz1EnwXXTuJCVbni06jluYIVFiJxnCVLN9JdYbMmXgypq9N6jtE+DLFxpnYEqX+a4tbYR2nVHJ+k5ph+p2AsZJHVJmZLST+Ceo/J0J3PkW77xdOovpOZV+pXY8mScNnD6b6jB+0mlbFe3qzpAqCEMSL2uJzxupWXkyvxHVjC+mGOjnLpB2ryzoONzdEJuZh896rOohDMtjc5dzcsZWNUvuZoafQKPMiGeaMfpJ2YZq9X8xvKuo0UzRkm804RUVSM/Nlch6gdx7idT6UxV0C322nLaAmlyrNDTA3lTWY3ONIuaKlFp+TrK1b+0Q+9zeY7CdUDgyaOokO15jPTzj4LdfBd0alto49S8pEzhP3hEVs6TsYPTk30HaW9euAJXpilHcTN5rnt7gGU6Zsx2liGlm1YHOMezdvmKqLk3lJj86TeZbEZi3F5V1a5PJlrFovkinnjEsM1zQvt2lM7Q2aNXmljgoqkZ2fM5sdQxYjaRfaFiRfAi8EKCEQfvDBjSsYrVFomUh28BMb1Qix8QUM5hs28UZHKkxWkxqQim+eA2IjbN4jnwzFLThtIXbKQmgLG8napG0wlcjbkRH7iaD2cMmBoeqMK8MtI9pPvHWqWk/B17rKh3isLiCp42nSx3Ejc6dE7FvKxjJdepeQmhxqkGcnQgmETDIPiNlTJkVZNiWN4arFrTMdVIXKhYwcnyKRbSRTbaNWhBrSJ8lyL2EkPD+MfMjh4GaJtJPUJP4hvJgGJPmRbwFp2xAeRi6lQmIR7GNs0aLbyRR4IJ5KZIdrxhoC8bZo0URSnYTNEiC0WqxyLti1ENjtBCYxR+kJgh3gnC8DohwQRCdBwxBBAOg4cEE4dAEOCCAILwWggnHAtDtBBOCGEhhRBBODSDsIRUQQRQh6RBpEEE46kFYQrCHBCcEYRAhQQisK0KCCEVhQiYIIRWJNok2gghRHIBtEkiCCMRMTeEWggjCBaoawQTmAOCCCKE//9k=',58,'26687beae8a35a36c1c96acb70b3836b377f57a21b8a5d9030e41cf5a82696ced00d962bc37d7852e2e4f389ac8416cd392bb51854c1f41d2f992b476006d919','2021-07-03','OSiLPEf9gl'),('coffee','coffee@mail.com','I am a coffee','2021-07-14','https://upload.wikimedia.org/wikipedia/commons/4/45/A_small_cup_of_coffee.JPG','https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Coffee_beans2.jpg/220px-Coffee_beans2.jpg',59,'c9ec7cd5c7ab0d1ea25fa12ac83c4a6be1fcabaaf7aab747c3a64989469dd737b0d68b08a913f83874a10459aa045e1e5288ba13f950c098c99e16a09e33ca67','2021-07-03','pzsNzxqav3'),('tea','hi@me.com','I am tea','2021-05-06',NULL,NULL,60,'f28f6a9429d4b763bed23b4030ffc4dd75ff36f00d89bf05f5543c5579f259fa1aa293aa9217e27a42ec2a0a5553153c0da429e2e25999eee716443d57184e5b','2021-07-03','eRtyVtBhY2');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'tweeter2'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-09 18:27:15
