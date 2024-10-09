-- --------------------------------------------------------
-- Host:                         103.181.129.19
-- Versi server:                 5.5.68-MariaDB - MariaDB Server
-- OS Server:                    Linux
-- HeidiSQL Versi:               12.5.0.6677
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- membuang struktur untuk table pkbtabalong.web_sistem
CREATE TABLE IF NOT EXISTS `web_sistem` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `logo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `alamat` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gambar_header` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telp` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `instagram` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `facebook` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `twitter` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `maps` text COLLATE utf8mb4_unicode_ci,
  `id_user` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Membuang data untuk tabel pkbtabalong.web_sistem: ~1 rows (lebih kurang)
REPLACE INTO `web_sistem` (`id`, `logo`, `nama`, `alamat`, `gambar_header`, `telp`, `email`, `instagram`, `facebook`, `twitter`, `maps`, `id_user`, `created_at`, `updated_at`) VALUES
	(1, 'logo-header.png', 'Dinas Perhubungan Kabupaten Tabalong', 'Jl. Mabu’un Raya No. 39, Maburai, Murung Pudak, Maburai, Kec. Murung Pudak, Kabupaten Tabalong, Kalimantan Selatan 71571', '20220922204134.jpg', '1234567980', 'dishub@email.id', 'https://www.instagram.com/', 'https://www.facebook.com/', 'https://twitter.com/', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3986.936142915355!2d115.43098721526935!3d-2.1779483378642777!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dfab251f077a125%3A0xfc6d4a5257952f84!2sKantor%20Dinas%20Perhubungan%2C%20Komunikasi%20dan%20Informatika%20Kabupaten%20Tabalong!5e0!3m2!1sen!2sid!4v1665589571729!5m2!1sen!2sid', 1, '2022-08-05 12:40:19', '2022-10-12 14:47:43');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
