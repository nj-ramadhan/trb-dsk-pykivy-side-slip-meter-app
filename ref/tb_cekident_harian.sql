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

-- membuang struktur untuk table pkbtabalong.tb_cekident
CREATE TABLE IF NOT EXISTS `tb_cekident` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `noantrian` varchar(11) DEFAULT NULL,
  `nouji` varchar(255) DEFAULT NULL,
  `NEW_NOUJI` varchar(20) DEFAULT NULL,
  `nopol` varchar(255) DEFAULT NULL,
  `statusuji` varchar(11) DEFAULT NULL,
  `statuspenerbitan` varchar(1) DEFAULT NULL,
  `idjeniskendaraan` varchar(255) DEFAULT NULL,
  `kd_jnskendaraan` varchar(4) DEFAULT NULL,
  `kodewilayah` varchar(50) DEFAULT NULL,
  `jenis` varchar(255) DEFAULT NULL,
  `merk` varchar(255) DEFAULT NULL,
  `statusmaster` char(2) DEFAULT NULL,
  `tgl_daftar` datetime DEFAULT NULL,
  `user` varchar(255) DEFAULT NULL,
  `kode_daerah` varchar(255) DEFAULT NULL,
  `no_kendaraan` varchar(50) DEFAULT NULL,
  `kode_huruf` varchar(255) DEFAULT NULL,
  `nopol_lama` varchar(255) DEFAULT NULL,
  `catatan` text,
  `type` varchar(255) DEFAULT NULL,
  `id_img` int(11) DEFAULT NULL,
  `sts` char(1) DEFAULT '0',
  `jbb` int(11) DEFAULT NULL,
  `flag` char(1) DEFAULT NULL,
  `statusdata` char(1) DEFAULT NULL,
  `wilayahasal` varchar(255) DEFAULT 'TBLNG',
  `asaluji` varchar(255) DEFAULT 'TBLNG',
  `vabank` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

-- Membuang data untuk tabel pkbtabalong.tb_cekident: ~13 rows (lebih kurang)
REPLACE INTO `tb_cekident` (`id`, `noantrian`, `nouji`, `NEW_NOUJI`, `nopol`, `statusuji`, `statuspenerbitan`, `idjeniskendaraan`, `kd_jnskendaraan`, `kodewilayah`, `jenis`, `merk`, `statusmaster`, `tgl_daftar`, `user`, `kode_daerah`, `no_kendaraan`, `kode_huruf`, `nopol_lama`, `catatan`, `type`, `id_img`, `sts`, `jbb`, `flag`, `statusdata`, `wilayahasal`, `asaluji`, `vabank`) VALUES
	(2, '0001', 'CB09C12001835', 'CB09C12001835', 'DA8114HG', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A11', 'MT', '0', '2024-08-16 07:34:01', 'HUSNA', 'HG', '8114', 'DA', NULL, NULL, 'T120 SS', 331541, '1', 1760, '1', '1', 'TBLNG', 'TBLNG', NULL),
	(3, '0002', 'CC0111298', 'CC0111298', 'KH8513AK', 'ND', '5', 'Mobil Barang Bak Tertutup', 'C', 'TBLNG', 'A23', 'MT', '0', '2024-08-16 07:40:17', 'NOVITASARI', 'KH', '8513', 'AK', '', '', 'FE73', NULL, '1', 7000, NULL, '1', 'TBLNG', 'PLANK', NULL),
	(4, '0003', 'CB71C2351522', 'CB71C2351522', 'DA8119HH', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A12', 'MT', '0', '2024-08-16 07:43:24', 'HUSNA', 'HH', '8119', 'DA', NULL, NULL, 'TRITON DC-CR25', 330824, '1', 2850, '1', '1', 'TBLNG', 'TBLNG', NULL),
	(5, '0004', 'CB09C12002410', 'CB09C12002410', 'DA8165HD', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A11', 'SZ', '0', '2024-08-16 07:47:05', NULL, 'HD', '8165', 'DA', NULL, NULL, 'ST150', 332157, '1', 2085, '1', '1', 'TBLNG', 'TBLNG', NULL),
	(6, '0005', 'CB09C23008656', 'CB09C23008656', 'DA8760HJ', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A12', 'MT', '0', '2024-08-16 08:00:49', 'HUSNA', 'DA', '8760', 'HJ', NULL, NULL, 'TRITON DC-CR25', 331965, '1', 2850, '1', '1', 'TBLNG', 'TBLNG', NULL),
	(7, '0006', 'CB09C24008998', 'CB09C24008998', 'DA8253HH', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A12', 'MT', '0', '2024-08-16 08:04:38', 'HUSNA', 'DA', '8253', 'HH', NULL, NULL, 'TRITON DC-CR25', 332158, '1', 2850, '1', '1', 'TBLNG', 'TBLNG', NULL),
	(8, '0007', 'CB09C24009000', 'CB09C24009000', 'DA8327HH', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A12', 'MT', '0', '2024-08-16 08:22:24', 'HUSNA', 'DA', '8327', 'HH', NULL, NULL, 'TRITON DC-CR25', 332161, '1', 2850, '1', '1', 'TBLNG', 'TBLNG', NULL),
	(9, '0008', 'CB09B15005407', 'CB09B15005407', 'DA7012HG', 'B', '2', 'Mobil Bus Sedang', 'B', 'TBLNG', 'B21', 'IZ', '0', '2024-08-16 08:33:22', NULL, 'HG', '7012', 'DA', NULL, NULL, 'NHR 55', 332056, '1', 5100, '1', '1', 'TBLNG', 'TBLNG', NULL),
	(10, '0009', 'CB09B13003976', 'CB09B13003976', 'DA7319HB', 'B', '2', 'Mobil Bus Sedang', 'B', 'TBLNG', 'B21', 'MT', '0', '2024-08-16 08:34:24', 'HUSNA', 'HB', '7319', 'DA', NULL, NULL, 'BUS FE 74', 332053, '1', 7500, '1', '1', 'TBLNG', 'TBLNG', NULL),
	(11, '0010', 'CB09C18006631', 'CB09C18006631', 'DA8032HC', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A12', 'MT', '0', '2024-08-16 08:35:14', 'HUSNA', 'HC', '8032', 'DA', NULL, NULL, 'TRITON DC-CR25', 332239, '1', 2730, '1', '1', 'TBLNG', 'TBLNG', NULL),
	(12, '0011', 'CB09C23008771', 'CB09C23008771', 'DA8803HJ', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A11', 'SZ', '0', '2024-08-16 08:38:32', 'HUSNA', 'DA', '8803', 'HJ', NULL, NULL, 'AEV415W CX 4X2 M/T', 332127, '1', 2190, '1', '1', 'TBLNG', 'TBLNG', NULL),
	(13, '0012', 'CB09B19007471', 'CB09B19007471', 'DA7568HB', 'B', '2', 'Mobil Bus Sedang', 'B', 'TBLNG', 'B21', 'IZ', '0', '2024-08-16 08:42:10', 'HUSNA', 'HB', '7568', 'DA', NULL, NULL, 'NLR 55B LX 4x2 M/T', 329006, '1', 5100, '1', '1', 'TBLNG', 'TBLNG', NULL),
	(14, '0013', 'CB09B18006930', 'CB09B18006930', 'DA7367HB', 'B', '2', 'Mobil Bus Sedang', 'B', 'TBLNG', 'B21', 'MT', '0', '2024-08-16 09:28:50', NULL, 'HB', '7367', 'DA', NULL, NULL, 'FE 84', 332139, '1', 8000, '1', '1', 'TBLNG', 'TBLNG', NULL);

-- membuang struktur untuk table pkbtabalong.users
CREATE TABLE IF NOT EXISTS `users` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `username` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `password` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `typex` smallint(6) NOT NULL DEFAULT '0' COMMENT '1=admin, 2=penguji, 3=operator loket 1, 4=operator loket 2, 5=operator loket 3',
  `type` smallint(6) NOT NULL COMMENT '1=admin, 2=operator',
  `nip` varchar(50) COLLATE latin1_general_ci DEFAULT NULL,
  `image` varchar(50) COLLATE latin1_general_ci DEFAULT 'free.jpg',
  `image_ttd` varchar(50) COLLATE latin1_general_ci DEFAULT 'free.jpg',
  `sts` int(11) DEFAULT '1',
  `kode_cab` int(11) DEFAULT '0',
  `id_pegawai` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_user`)
) ENGINE=MyISAM AUTO_INCREMENT=80 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Membuang data untuk tabel pkbtabalong.users: 12 rows
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
REPLACE INTO `users` (`id_user`, `nama`, `username`, `password`, `typex`, `type`, `nip`, `image`, `image_ttd`, `sts`, `kode_cab`, `id_pegawai`) VALUES
	(42, 'PARJANTO, S.Sos', 'parjanto', '53d2732235a18d187f5f41a301e0cc1f', 2, 8, '063.009.PT3.01.001', 'parjanto.jpg', NULL, 1, 0, 42),
	(70, 'CANDRA LUKITO, A.MA', 'lukito', 'cd40d10e7b45793a148bd7ddafdc18c6', 2, 8, '063.009.PT2.01.001', 'chandra.jpg', NULL, 1, 0, 40),
	(79, 'DJATMIKO', 'miko', 'ef9322a1a342a36856e9e8929b19437a', 2, 8, '19691013 199403 1 010', 'miko.jpg', NULL, 1, 0, 38);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
