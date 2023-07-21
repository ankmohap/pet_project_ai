CREATE TABLE `client` (
  `name` varchar(30) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `city` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `orders` (
  `order_cd` varchar(30) DEFAULT NULL,
  `client_name` varchar(30) DEFAULT NULL,
  `amount` decimal(10,0) DEFAULT NULL,
  `product_name` varchar(30) DEFAULT NULL,
  `product_cd` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
