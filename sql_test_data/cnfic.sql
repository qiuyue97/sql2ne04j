-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: cnfic
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `t_annual_basicinfo`
--

DROP TABLE IF EXISTS `t_annual_basicinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_annual_basicinfo` (
  `id` varchar(64) DEFAULT NULL,
  `key_no` varchar(64) DEFAULT NULL,
  `company_id` varchar(64) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `reg_no` varchar(64) DEFAULT NULL,
  `operator_name` varchar(128) DEFAULT NULL,
  `contact_no` varchar(2048) DEFAULT NULL,
  `post_code` varchar(64) DEFAULT NULL,
  `address` varchar(2048) DEFAULT NULL,
  `email_address` varchar(4096) DEFAULT NULL,
  `is_stock_right_transfer` varchar(64) DEFAULT NULL,
  `status` varchar(64) DEFAULT NULL,
  `has_website` varchar(8) DEFAULT NULL,
  `has_new_stock_or_by_stock` varchar(8) DEFAULT NULL,
  `employee_count` varchar(128) DEFAULT NULL,
  `belong_to` varchar(128) DEFAULT NULL,
  `capital_amount` varchar(64) DEFAULT NULL,
  `has_provide_assurance` varchar(8) DEFAULT NULL,
  `operation_places` varchar(128) DEFAULT NULL,
  `main_type` varchar(64) DEFAULT NULL,
  `operation_duration` varchar(64) DEFAULT NULL,
  `if_content_same` varchar(8) DEFAULT NULL,
  `different_content` varchar(512) DEFAULT NULL,
  `general_operation_item` varchar(1024) DEFAULT NULL,
  `approved_operation_item` varchar(2048) DEFAULT NULL,
  `credit_code` varchar(64) DEFAULT NULL,
  `dates` varchar(10) DEFAULT NULL,
  `isadd` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_annual_basicinfo`
--

LOCK TABLES `t_annual_basicinfo` WRITE;
/*!40000 ALTER TABLE `t_annual_basicinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_annual_basicinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_annual_report`
--

DROP TABLE IF EXISTS `t_annual_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_annual_report` (
  `id` varchar(64) DEFAULT NULL,
  `key_no` varchar(64) DEFAULT NULL,
  `company_id` varchar(64) DEFAULT NULL,
  `no` varchar(8) DEFAULT NULL,
  `year` varchar(64) DEFAULT NULL,
  `remarks` varchar(512) DEFAULT NULL,
  `publish_date` varchar(30) DEFAULT NULL,
  `dates` varchar(10) DEFAULT NULL,
  `isadd` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_annual_report`
--

LOCK TABLES `t_annual_report` WRITE;
/*!40000 ALTER TABLE `t_annual_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_annual_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_bidding_baseinfo`
--

DROP TABLE IF EXISTS `t_bidding_baseinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_bidding_baseinfo` (
  `projectId` varchar(255) DEFAULT NULL,
  `docIds` varchar(255) DEFAULT NULL,
  `docId` varchar(255) DEFAULT NULL,
  `province` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `persistenceTime` varchar(255) DEFAULT NULL,
  `pageTime` varchar(255) DEFAULT NULL,
  `docChannel` varchar(255) DEFAULT NULL,
  `biddingBudget` varchar(255) DEFAULT NULL,
  `winBidPrice` varchar(255) DEFAULT NULL,
  `totalTendereeMoney` varchar(255) DEFAULT NULL,
  `docTitle` varchar(255) DEFAULT NULL,
  `projectName` varchar(255) DEFAULT NULL,
  `projectCode` varchar(255) DEFAULT NULL,
  `product` varchar(255) DEFAULT NULL,
  `winTenderer` varchar(255) DEFAULT NULL,
  `tenderee` varchar(255) DEFAULT NULL,
  `agency` varchar(255) DEFAULT NULL,
  `products` varchar(255) DEFAULT NULL,
  `moneySource` varchar(255) DEFAULT NULL,
  `personReview` varchar(255) DEFAULT NULL,
  `system` varchar(255) DEFAULT NULL,
  `bidWay` varchar(255) DEFAULT NULL,
  `industry` varchar(255) DEFAULT NULL,
  `infoType` varchar(255) DEFAULT NULL,
  `qName` varchar(255) DEFAULT NULL,
  `serviceTime` varchar(255) DEFAULT NULL,
  `webSourceName` varchar(255) DEFAULT NULL,
  `detailLink` varchar(255) DEFAULT NULL,
  `winTendererManager` varchar(255) DEFAULT NULL,
  `winTendererPhone` varchar(255) DEFAULT NULL,
  `tendereeContact` varchar(255) DEFAULT NULL,
  `tendereePhone` varchar(255) DEFAULT NULL,
  `agencyContact` varchar(255) DEFAULT NULL,
  `agencyPhone` varchar(255) DEFAULT NULL,
  `secondTenderer` varchar(255) DEFAULT NULL,
  `secondBidPrice` varchar(255) DEFAULT NULL,
  `thirdTenderer` varchar(255) DEFAULT NULL,
  `thirdBidPrice` varchar(255) DEFAULT NULL,
  `timeBidClose` varchar(255) DEFAULT NULL,
  `timeBidOpen` varchar(255) DEFAULT NULL,
  `timeRelease` varchar(255) DEFAULT NULL,
  `timeBidStart` varchar(255) DEFAULT NULL,
  `timePublicityStart` varchar(255) DEFAULT NULL,
  `timePublicityEnd` varchar(255) DEFAULT NULL,
  `timeGetFileStart` varchar(255) DEFAULT NULL,
  `timeGetFileEnd` varchar(255) DEFAULT NULL,
  `timeRegistrationStart` varchar(255) DEFAULT NULL,
  `timeRegistrationEnd` varchar(255) DEFAULT NULL,
  `timeEarnestMoneyStart` varchar(255) DEFAULT NULL,
  `timeEarnestMoneyEnd` varchar(255) DEFAULT NULL,
  `timeCommencement` varchar(255) DEFAULT NULL,
  `timeCompletion` varchar(255) DEFAULT NULL,
  `tenderType` varchar(255) DEFAULT NULL,
  `docHtmlCon` varchar(255) DEFAULT NULL,
  `docTextCon` varchar(255) DEFAULT NULL,
  `pageAttachments` varchar(255) DEFAULT NULL,
  `companyName` varchar(255) DEFAULT NULL,
  `companyCreditCode` varchar(255) DEFAULT NULL,
  `pushType` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_bidding_baseinfo`
--

LOCK TABLES `t_bidding_baseinfo` WRITE;
/*!40000 ALTER TABLE `t_bidding_baseinfo` DISABLE KEYS */;
INSERT INTO `t_bidding_baseinfo` VALUES (NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2024.5.6',NULL,NULL,'1000000',NULL,NULL,NULL,NULL,NULL,'外部公司1','分公司',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2024.5.7',NULL,NULL,'500000',NULL,NULL,NULL,NULL,NULL,'外部公司2','母公司',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `t_bidding_baseinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_company_control_person`
--

DROP TABLE IF EXISTS `t_company_control_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_company_control_person` (
  `id` varchar(64) NOT NULL,
  `key_no` varchar(64) DEFAULT NULL,
  `company_id` varchar(64) DEFAULT NULL,
  `oper_key_no` varchar(64) DEFAULT NULL,
  `oper_name` varchar(512) DEFAULT NULL,
  `node_type` varchar(512) DEFAULT NULL,
  `stock_percent` varchar(512) DEFAULT NULL,
  `dates` varchar(8) DEFAULT NULL,
  `isadd` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_company_control_person`
--

LOCK TABLES `t_company_control_person` WRITE;
/*!40000 ALTER TABLE `t_company_control_person` DISABLE KEYS */;
INSERT INTO `t_company_control_person` VALUES ('1','1','id_1','3','母公司','company','70%',NULL,NULL),('2','2','id_2','1','示例公司','company','50%',NULL,NULL),('3','3','id_3','1','刘一','person','10%',NULL,NULL);
/*!40000 ALTER TABLE `t_company_control_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_eci_branch`
--

DROP TABLE IF EXISTS `t_eci_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_eci_branch` (
  `id` varchar(64) DEFAULT NULL,
  `key_no` varchar(64) DEFAULT NULL,
  `company_id` varchar(64) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `sub_key_no` varchar(64) DEFAULT NULL,
  `sub_company_id` varchar(64) DEFAULT NULL,
  `name` varchar(512) DEFAULT NULL,
  `reg_no` varchar(64) DEFAULT NULL,
  `belong_org` varchar(255) DEFAULT NULL,
  `dates` varchar(10) DEFAULT NULL,
  `isadd` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_eci_branch`
--

LOCK TABLES `t_eci_branch` WRITE;
/*!40000 ALTER TABLE `t_eci_branch` DISABLE KEYS */;
INSERT INTO `t_eci_branch` VALUES ('1','1','id_1','示例公司','6','id_6','分公司',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `t_eci_branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_eci_company`
--

DROP TABLE IF EXISTS `t_eci_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_eci_company` (
  `key_no` varchar(64) DEFAULT NULL,
  `company_id` varchar(64) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `oper_key_no` varchar(64) DEFAULT NULL,
  `oper_name` varchar(512) DEFAULT NULL,
  `regist_capi` varchar(128) DEFAULT NULL,
  `regist_capi_value` varchar(128) DEFAULT NULL,
  `regist_capi_unit` varchar(128) DEFAULT NULL,
  `rec_cap` varchar(128) DEFAULT NULL,
  `status` varchar(128) DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `credit_code` varchar(128) DEFAULT NULL,
  `no` varchar(64) DEFAULT NULL,
  `econ_kind` varchar(64) DEFAULT NULL,
  `econ_kind_code` varchar(64) DEFAULT NULL,
  `check_date` datetime DEFAULT NULL,
  `belong_org` varchar(64) DEFAULT NULL,
  `province_code` varchar(8) DEFAULT NULL,
  `province` varchar(64) DEFAULT NULL,
  `term_start` datetime DEFAULT NULL,
  `term_end` datetime DEFAULT NULL,
  `address` varchar(512) DEFAULT NULL,
  `scope` varchar(4096) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  `dates` varchar(10) DEFAULT NULL,
  `isadd` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_eci_company`
--

LOCK TABLES `t_eci_company` WRITE;
/*!40000 ALTER TABLE `t_eci_company` DISABLE KEYS */;
INSERT INTO `t_eci_company` VALUES ('1','id_1','示例公司','2','陈二',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'1','北京',NULL,NULL,'adress1',NULL,'phone1',NULL,NULL,NULL),('2','id_2','子公司','3','张三',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2','上海',NULL,NULL,'adress2',NULL,'phone2',NULL,NULL,NULL),('3','id_3','母公司','4','李四',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2','上海',NULL,NULL,'adress3',NULL,'phone3',NULL,NULL,NULL),('4','id_4','外部公司1','9','吴九',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'3','广东',NULL,NULL,'adress4',NULL,'phone3',NULL,NULL,NULL),('5','id_5','外部公司2','10','郑十',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'4','江苏',NULL,NULL,'adress2',NULL,'phone4',NULL,NULL,NULL);
/*!40000 ALTER TABLE `t_eci_company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_eci_employee`
--

DROP TABLE IF EXISTS `t_eci_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_eci_employee` (
  `id` varchar(64) NOT NULL,
  `key_no` varchar(64) DEFAULT NULL,
  `company_id` varchar(64) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `job` varchar(128) DEFAULT NULL,
  `p_key_no` varchar(64) DEFAULT NULL,
  `dates` varchar(10) DEFAULT NULL,
  `isadd` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_eci_employee`
--

LOCK TABLES `t_eci_employee` WRITE;
/*!40000 ALTER TABLE `t_eci_employee` DISABLE KEYS */;
INSERT INTO `t_eci_employee` VALUES ('1','1','id_1','示例公司','李四','董事','4',NULL,NULL),('2','2','id_2','子公司','王五','监事','5',NULL,NULL),('3','3','id_3','母公司','王五','高管','5',NULL,NULL);
/*!40000 ALTER TABLE `t_eci_employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_eci_partner`
--

DROP TABLE IF EXISTS `t_eci_partner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_eci_partner` (
  `id` varchar(64) DEFAULT NULL,
  `key_no` varchar(64) DEFAULT NULL,
  `company_id` varchar(64) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `stock_name` varchar(255) DEFAULT NULL,
  `stock_type` varchar(128) DEFAULT NULL,
  `stock_percent` varchar(64) DEFAULT NULL,
  `should_capi` varchar(512) DEFAULT NULL,
  `should_capi_value` varchar(512) DEFAULT NULL,
  `should_capi_unit` varchar(512) DEFAULT NULL,
  `shoud_date` varchar(1024) DEFAULT NULL,
  `invest_type` varchar(1024) DEFAULT NULL,
  `invest_name` varchar(512) DEFAULT NULL,
  `real_capi` varchar(1024) DEFAULT NULL,
  `real_capi_value` varchar(1024) DEFAULT NULL,
  `real_capi_unit` varchar(1024) DEFAULT NULL,
  `capi_date` varchar(1024) DEFAULT NULL,
  `p_key_no` varchar(64) DEFAULT NULL,
  `dates` varchar(10) DEFAULT NULL,
  `isadd` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_eci_partner`
--

LOCK TABLES `t_eci_partner` WRITE;
/*!40000 ALTER TABLE `t_eci_partner` DISABLE KEYS */;
INSERT INTO `t_eci_partner` VALUES ('1','1','id_1','示例公司','刘一','person','30%','30',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'1',NULL,NULL),('2','1','id_1','示例公司','母公司','company','70%','70',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'3',NULL,NULL),('3','2','id_2','子公司','示例公司','company','50%','10',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'1',NULL,NULL),('4','3','id_3','母公司','刘一','person','10%','500',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'1',NULL,NULL);
/*!40000 ALTER TABLE `t_eci_partner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_stockrelation_invest_info`
--

DROP TABLE IF EXISTS `t_stockrelation_invest_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_stockrelation_invest_info` (
  `id` varchar(64) DEFAULT NULL,
  `key_no` varchar(64) DEFAULT NULL,
  `company_id` varchar(64) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `p_key_no` varchar(64) DEFAULT NULL,
  `stock_name` varchar(255) DEFAULT NULL,
  `stock_type` varchar(128) DEFAULT NULL,
  `stock_percent` varchar(64) DEFAULT NULL,
  `should_capi` varchar(512) DEFAULT NULL,
  `should_capi_value` varchar(512) DEFAULT NULL,
  `should_capi_unit` varchar(512) DEFAULT NULL,
  `shoud_date` varchar(1024) DEFAULT NULL,
  `regist_capi` varchar(512) DEFAULT NULL,
  `regist_capi_value` varchar(512) DEFAULT NULL,
  `regist_capi_unit` varchar(128) DEFAULT NULL,
  `province` varchar(64) DEFAULT NULL,
  `industry` varchar(64) DEFAULT NULL,
  `no` varchar(64) DEFAULT NULL,
  `credit_code` varchar(128) DEFAULT NULL,
  `oper_name` varchar(512) DEFAULT NULL,
  `status` varchar(128) DEFAULT NULL,
  `econ_kind` varchar(64) DEFAULT NULL,
  `dates` varchar(10) DEFAULT NULL,
  `isadd` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_stockrelation_invest_info`
--

LOCK TABLES `t_stockrelation_invest_info` WRITE;
/*!40000 ALTER TABLE `t_stockrelation_invest_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_stockrelation_invest_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_stockrelation_legal_info`
--

DROP TABLE IF EXISTS `t_stockrelation_legal_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_stockrelation_legal_info` (
  `key_no` varchar(64) DEFAULT NULL,
  `company_id` varchar(64) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `oper_key_no` varchar(64) DEFAULT NULL,
  `oper_name` varchar(512) DEFAULT NULL,
  `regist_capi` varchar(128) DEFAULT NULL,
  `regist_capi_value` varchar(128) DEFAULT NULL,
  `regist_capi_unit` varchar(128) DEFAULT NULL,
  `province_code` varchar(8) DEFAULT NULL,
  `province` varchar(64) DEFAULT NULL,
  `industry` varchar(64) DEFAULT NULL,
  `no` varchar(64) DEFAULT NULL,
  `credit_code` varchar(128) DEFAULT NULL,
  `status` varchar(128) DEFAULT NULL,
  `econ_kind` varchar(64) DEFAULT NULL,
  `dates` varchar(10) DEFAULT NULL,
  `isadd` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_stockrelation_legal_info`
--

LOCK TABLES `t_stockrelation_legal_info` WRITE;
/*!40000 ALTER TABLE `t_stockrelation_legal_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_stockrelation_legal_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_stockrelation_office_info`
--

DROP TABLE IF EXISTS `t_stockrelation_office_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_stockrelation_office_info` (
  `id` varchar(64) DEFAULT NULL,
  `key_no` varchar(64) DEFAULT NULL,
  `company_id` varchar(64) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `p_key_no` varchar(64) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `position` varchar(128) DEFAULT NULL,
  `regist_capi` varchar(128) DEFAULT NULL,
  `regist_capi_unit` varchar(128) DEFAULT NULL,
  `province` varchar(64) DEFAULT NULL,
  `industry` varchar(64) DEFAULT NULL,
  `no` varchar(64) DEFAULT NULL,
  `credit_code` varchar(128) DEFAULT NULL,
  `oper_name` varchar(512) DEFAULT NULL,
  `status` varchar(128) DEFAULT NULL,
  `econ_kind` varchar(64) DEFAULT NULL,
  `dates` varchar(10) DEFAULT NULL,
  `isadd` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_stockrelation_office_info`
--

LOCK TABLES `t_stockrelation_office_info` WRITE;
/*!40000 ALTER TABLE `t_stockrelation_office_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_stockrelation_office_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-26 11:25:27
