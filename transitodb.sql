-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 28-06-2019 a las 03:08:32
-- Versión del servidor: 5.7.26
-- Versión de PHP: 7.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `transitodb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `brands`
--

DROP TABLE IF EXISTS `brands`;
CREATE TABLE IF NOT EXISTS `brands` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `brand` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `brands`
--

INSERT INTO `brands` (`id`, `brand`) VALUES
(1, 'ALFA ROMEO'),
(2, 'AUDI'),
(3, 'BMW'),
(4, 'CHEVROLET'),
(5, 'CITROËN'),
(6, 'FIAT'),
(7, 'FORD'),
(8, 'HONDA'),
(9, 'HYUNDAI'),
(10, 'JEEP'),
(11, 'KIA'),
(12, 'MAZDA'),
(13, 'MERCEDES-BENZ'),
(14, 'MITSUBISHI'),
(15, 'NISSAN'),
(16, 'PEUGEOT'),
(17, 'RENAULT'),
(18, 'SUZUKI'),
(19, 'VOLKSWAGEN');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `infractions`
--

DROP TABLE IF EXISTS `infractions`;
CREATE TABLE IF NOT EXISTS `infractions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dni_resp` int(11) NOT NULL,
  `domain` varchar(10) NOT NULL,
  `cause` varchar(50) NOT NULL,
  `agent` varchar(30) NOT NULL,
  `datea` timestamp NOT NULL,
  `place` varchar(50) NOT NULL,
  `mount` double NOT NULL,
  `paid` tinyint(1) NOT NULL,
  `paydate` timestamp NULL DEFAULT NULL,
  `erased` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_domain` (`domain`),
  KEY `fk_dni_resp` (`dni_resp`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `infractions`
--

INSERT INTO `infractions` (`id`, `dni_resp`, `domain`, `cause`, `agent`, `datea`, `place`, `mount`, `paid`, `paydate`, `erased`) VALUES
(1, 34868304, 'KQQ642', 'S/ LUCES', 'Juan Rodriguez', '2019-06-06 12:00:00', 'Plaza San Martín', 3500, 1, '2019-06-27 21:58:31', 0),
(2, 34868304, 'KQQ642', 'S/ PATENTE', 'Pedro Lopez', '2019-06-04 23:00:00', 'Plaza San Martín', 1500, 1, '2019-06-27 21:58:42', 0),
(3, 34868304, 'VPP720', 'S/ PATENTE', 'Juan Perez', '2013-03-10 13:15:00', '15 e/ 10 y 12', 4000, 1, '2019-06-27 21:54:18', 0),
(4, 34868304, 'KQQ642', 'S/ LUCES', 'Juan Perez', '2019-06-11 15:00:00', 'calle 12 e/ 5 y 7', 1000, 1, '2019-06-27 21:59:14', 0),
(9, 34868304, 'KQQ642', 'S/ LUCES', 'Juan Perez', '2019-06-13 06:00:00', 'Calle 21 y 16', 3000, 1, '2019-06-27 22:00:06', 0),
(10, 34868304, 'VPP720', 'S/ PATENTE', 'Pedro Dominguez', '2019-06-02 14:00:00', 'Calle 21 y 28', 2000, 0, NULL, 1),
(11, 34868304, 'KQQ642', 'S/ LUCES', 'Simón García', '2019-06-20 14:00:00', 'Calle 12 y 1', 3000, 0, NULL, 0),
(12, 34868304, 'KQQ642', 'S/ LUCES', 'Simon García', '2019-06-20 11:00:00', 'Calle 12 y 1', 10000, 0, NULL, 1),
(13, 34868304, 'VPP720', 'S/ CASCO', 'Alexis Fleitas', '2019-06-26 13:00:00', 'Calle 12 e/ 51', 3000, 1, '2019-06-27 19:24:58', 0),
(14, 34868304, 'KQQ642', 'S/ LUCES', 'Ramón Benitez', '2019-06-26 10:00:00', 'calle 24 e/ 31 y 33', 2500, 0, NULL, 0),
(15, 34868304, 'KQQ642', 'S/ PAPELES', 'Ramón Benitez', '2019-06-26 19:00:00', 'Calle 12 e/ 1', 1500.75, 0, NULL, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `models`
--

DROP TABLE IF EXISTS `models`;
CREATE TABLE IF NOT EXISTS `models` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `brand` int(11) NOT NULL,
  `model` varchar(30) NOT NULL,
  `kind` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_brand` (`brand`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `models`
--

INSERT INTO `models` (`id`, `brand`, `model`, `kind`) VALUES
(1, 1, 'MiTo', 'automovil'),
(2, 1, 'Giulietta', 'automovil'),
(3, 1, 'Giulia', 'automovil'),
(4, 1, '4C', 'automovil'),
(5, 1, 'Stelvio', 'automovil'),
(6, 1, 'Tonale', 'automovil'),
(7, 2, 'A1', 'automovil'),
(8, 2, 'A3', 'automovil'),
(9, 2, 'A4', 'automovil'),
(10, 2, 'A5', 'automovil'),
(11, 2, 'A7 Sportback', 'automovil'),
(12, 2, 'A8', 'automovil'),
(13, 2, 'TT', 'automovil'),
(14, 2, 'R8', 'automovil'),
(15, 3, 'Serie 1', 'automovil'),
(16, 3, 'Serie 2', 'automovil'),
(17, 3, 'Z4', 'automovil'),
(18, 3, 'X1', 'automovil'),
(19, 3, 'X7', 'automovil'),
(20, 3, 'i8', 'automovil'),
(21, 4, 'Aveo', 'automovil'),
(22, 4, 'Cobalt', 'automovil'),
(23, 4, 'Prisma', 'automovil'),
(24, 4, 'S10', 'camioneta'),
(25, 4, 'Corsa', 'automovil'),
(26, 4, 'Astra', ''),
(27, 5, 'C4', ''),
(28, 5, 'C4 Cactus', ''),
(29, 5, 'Berlingo', ''),
(30, 6, '500', 'automovil'),
(31, 6, 'Punto', 'automovil'),
(32, 6, 'TIPO', 'automovil'),
(33, 6, 'Panda', 'automovil'),
(34, 7, 'Ka', 'automovil'),
(35, 7, 'F100', 'camioneta'),
(36, 7, 'Fiesta', 'automovil'),
(37, 7, 'Focus', 'automovil'),
(38, 7, 'Mondeo', 'automovil'),
(39, 7, 'Ranger', 'camioneta'),
(40, 8, 'Civic', 'automovil'),
(41, 8, 'HR-V', 'automovil'),
(42, 9, 'Kona', 'automovil'),
(43, 9, 'NEXO', 'automovil'),
(44, 10, 'Renegade', 'automovil'),
(45, 10, 'Grand Cherokee', 'camioneta'),
(46, 11, 'Optima', 'automovil'),
(47, 11, 'Sorento', 'automovil'),
(48, 12, 'MX-5', 'automovil'),
(49, 12, 'CX-3', 'automovil'),
(50, 13, 'CLS', 'automovil'),
(51, 13, 'EQV', 'automovil'),
(52, 14, 'Space Star', 'automovil'),
(53, 14, 'Outlander', 'camioneta'),
(54, 14, 'L200', 'camioneta'),
(55, 15, 'Micra', 'automovil'),
(56, 15, 'Qashqai', 'automovil'),
(57, 16, '208', 'automovil'),
(58, 16, 'Rifter', 'automovil'),
(59, 17, 'Twingo', 'automovil'),
(60, 17, 'Mégane', 'automovil'),
(61, 18, 'Celerio', 'automovil'),
(62, 18, 'Swift', 'automovil'),
(63, 18, 'Vitara', 'automovil'),
(64, 19, 'Polo', 'automovil'),
(65, 19, 'Gol', 'automovil'),
(66, 19, 'Passat', 'automovil');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persons`
--

DROP TABLE IF EXISTS `persons`;
CREATE TABLE IF NOT EXISTS `persons` (
  `dni` int(11) NOT NULL,
  `surname` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `birth` timestamp NOT NULL,
  `residence` varchar(100) NOT NULL,
  `nationality` varchar(30) NOT NULL,
  `category` varchar(5) NOT NULL,
  `bloodtype` varchar(3) NOT NULL,
  `erased` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`dni`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `persons`
--

INSERT INTO `persons` (`dni`, `surname`, `name`, `birth`, `residence`, `nationality`, `category`, `bloodtype`, `erased`) VALUES
(34868304, 'Rolón', 'Lucas martin', '1990-12-15 03:00:00', 'Dorrego 1070', 'Argentino', 'C.3', 'A-', 0),
(34901010, 'Aquino', 'Sabrina romina', '1990-03-01 03:00:00', 'Pueyrredon 1183', 'Argentino', 'G.1', '0+', 1),
(34961209, 'Gomez', 'Pedro Pablo', '1990-03-01 03:00:00', 'Pueyrredón 1500', 'Argentino', 'A.3', '0+', 1),
(40034659, 'Romaniuk', 'Alexis agustín', '1997-02-21 03:00:00', 'Calle 6 y 11 E. Sur', 'Argentino', 'B.1', '0-', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `erased` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `user`, `password`, `erased`) VALUES
(1, 'admin', 'pass', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehicles`
--

DROP TABLE IF EXISTS `vehicles`;
CREATE TABLE IF NOT EXISTS `vehicles` (
  `domain` varchar(10) NOT NULL,
  `kind` varchar(15) NOT NULL,
  `brand` varchar(15) NOT NULL,
  `model` varchar(15) NOT NULL,
  `year` int(11) NOT NULL,
  `vin` varchar(20) NOT NULL,
  `owner` int(11) NOT NULL,
  `erased` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`domain`),
  KEY `fk_owner` (`owner`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `vehicles`
--

INSERT INTO `vehicles` (`domain`, `kind`, `brand`, `model`, `year`, `vin`, `owner`, `erased`) VALUES
('AS657HN', 'AUTOMÓVIL', 'AUDI', '4C', 2016, 'GFHDD64JD7182332', 34868304, 0),
('KQQ642', 'AUTOMOVIL', 'CHEVROLET', 'Aveo', 2011, '44GJD75JAK5U1132', 34868304, 0),
('LLL111', 'AUTOMÓVIL', 'HONDA', 'Civic', 1990, 'JFHS63UF461H5235', 34868304, 0),
('LLT763', 'AUTOMÓVIL', 'ALFA ROMEO', 'MiTo', 1969, 'JHALH657UY6M1111', 34868304, 0),
('VPP720', 'AUTOMOVIL', 'RENAULT', '9', 1993, '63682GHD63762345', 34868304, 0);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `infractions`
--
ALTER TABLE `infractions`
  ADD CONSTRAINT `fk_dni_resp` FOREIGN KEY (`dni_resp`) REFERENCES `persons` (`dni`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_domain` FOREIGN KEY (`domain`) REFERENCES `vehicles` (`domain`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `models`
--
ALTER TABLE `models`
  ADD CONSTRAINT `fk_brand` FOREIGN KEY (`brand`) REFERENCES `brands` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `vehicles`
--
ALTER TABLE `vehicles`
  ADD CONSTRAINT `fk_owner` FOREIGN KEY (`owner`) REFERENCES `persons` (`dni`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
