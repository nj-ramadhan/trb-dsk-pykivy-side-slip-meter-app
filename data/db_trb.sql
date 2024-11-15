-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 15, 2024 at 04:38 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_trb`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_cekident`
--

CREATE TABLE `tb_cekident` (
  `id` int(11) NOT NULL,
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
  `catatan` text DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `id_img` int(11) DEFAULT NULL,
  `sts` char(1) DEFAULT '0',
  `jbb` int(11) DEFAULT NULL,
  `flag` char(1) DEFAULT NULL,
  `statusdata` char(1) DEFAULT NULL,
  `wilayahasal` varchar(255) DEFAULT 'TBLNG',
  `asaluji` varchar(255) DEFAULT 'TBLNG',
  `vabank` char(50) DEFAULT NULL,
  `check_flag` smallint(1) NOT NULL DEFAULT 0,
  `check_body_flag` int(1) NOT NULL DEFAULT 0,
  `check_body_image` text DEFAULT NULL,
  `check_chassis_flag` int(1) NOT NULL DEFAULT 0,
  `check_chassis_image` text DEFAULT NULL,
  `check_engine_flag` int(1) NOT NULL DEFAULT 0,
  `check_engine_image` text DEFAULT NULL,
  `check_handle_flag` int(1) NOT NULL DEFAULT 0,
  `check_handle_image` text DEFAULT NULL,
  `check_wiper_flag` int(1) NOT NULL DEFAULT 0,
  `check_wiper_image` text DEFAULT NULL,
  `check_windshield_flag` int(1) NOT NULL DEFAULT 0,
  `check_windshield_image` text DEFAULT NULL,
  `check_headlight_flag` int(1) NOT NULL DEFAULT 0,
  `check_headlight_image` text DEFAULT NULL,
  `check_signallight_flag` int(1) NOT NULL DEFAULT 0,
  `check_signallight_image` text DEFAULT NULL,
  `check_user` int(11) DEFAULT NULL,
  `check_post` timestamp NULL DEFAULT current_timestamp(),
  `emission_flag` smallint(1) NOT NULL DEFAULT 0,
  `emission_value` float DEFAULT NULL,
  `emission_user` int(11) DEFAULT NULL,
  `emission_post` timestamp NULL DEFAULT current_timestamp(),
  `sideslip_flag` smallint(1) NOT NULL DEFAULT 0,
  `sideslip_value` float DEFAULT NULL,
  `sideslip_user` int(11) DEFAULT NULL,
  `sideslip_post` timestamp NULL DEFAULT current_timestamp(),
  `load_flag` smallint(1) DEFAULT 0,
  `load_l_value` float DEFAULT NULL,
  `load_r_value` float DEFAULT NULL,
  `load_user` int(11) DEFAULT NULL,
  `load_post` timestamp NULL DEFAULT current_timestamp(),
  `brake_flag` smallint(1) NOT NULL DEFAULT 0,
  `brake_value` float DEFAULT NULL,
  `brake_user` int(11) DEFAULT NULL,
  `brake_post` timestamp NULL DEFAULT current_timestamp(),
  `speed_flag` smallint(1) NOT NULL DEFAULT 0,
  `speed_value` float DEFAULT NULL,
  `speed_user` int(11) DEFAULT NULL,
  `speed_post` timestamp NULL DEFAULT current_timestamp(),
  `hlm_flag` smallint(1) NOT NULL DEFAULT 0,
  `hlm_value` float DEFAULT NULL,
  `hlm_user` int(11) DEFAULT NULL,
  `hlm_post` timestamp NULL DEFAULT current_timestamp(),
  `slm_flag` smallint(1) NOT NULL DEFAULT 0,
  `slm_value` float DEFAULT NULL,
  `slm_user` int(11) DEFAULT NULL,
  `slm_post` timestamp NULL DEFAULT current_timestamp(),
  `wtm_flag` smallint(1) NOT NULL DEFAULT 0,
  `wtm_value` float DEFAULT NULL,
  `wtm_user` int(11) DEFAULT NULL,
  `wtm_post` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `tb_cekident`
--

INSERT INTO `tb_cekident` (`id`, `noantrian`, `nouji`, `NEW_NOUJI`, `nopol`, `statusuji`, `statuspenerbitan`, `idjeniskendaraan`, `kd_jnskendaraan`, `kodewilayah`, `jenis`, `merk`, `statusmaster`, `tgl_daftar`, `user`, `kode_daerah`, `no_kendaraan`, `kode_huruf`, `nopol_lama`, `catatan`, `type`, `id_img`, `sts`, `jbb`, `flag`, `statusdata`, `wilayahasal`, `asaluji`, `vabank`, `check_flag`, `check_body_flag`, `check_body_image`, `check_chassis_flag`, `check_chassis_image`, `check_engine_flag`, `check_engine_image`, `check_handle_flag`, `check_handle_image`, `check_wiper_flag`, `check_wiper_image`, `check_windshield_flag`, `check_windshield_image`, `check_headlight_flag`, `check_headlight_image`, `check_signallight_flag`, `check_signallight_image`, `check_user`, `check_post`, `emission_flag`, `emission_value`, `emission_user`, `emission_post`, `sideslip_flag`, `sideslip_value`, `sideslip_user`, `sideslip_post`, `load_flag`, `load_l_value`, `load_r_value`, `load_user`, `load_post`, `brake_flag`, `brake_value`, `brake_user`, `brake_post`, `speed_flag`, `speed_value`, `speed_user`, `speed_post`, `hlm_flag`, `hlm_value`, `hlm_user`, `hlm_post`, `slm_flag`, `slm_value`, `slm_user`, `slm_post`, `wtm_flag`, `wtm_value`, `wtm_user`, `wtm_post`) VALUES
(2, '0001', 'CB09C12001835', 'CB09C12001835', 'DA8114HG', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A11', 'MT', '0', '2024-08-16 07:34:01', 'HUSNA', 'HG', '8114', 'DA', NULL, NULL, 'T120 SS', 331541, '2', 1760, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 2, 12, 1, '2024-11-01 15:44:12', 1, 0, 0, 1, '2024-11-14 14:32:10', 0, NULL, NULL, '2024-11-01 15:02:20', 2, 0, 1, '2024-11-14 14:08:17', 0, 50.7, 1, '2024-11-15 15:26:53', 0, 95.7396, 1, '2024-09-01 10:25:07', 0, 0, 0, '2024-09-24 02:42:53'),
(3, '0002', 'CC0111298', 'CC0111298', 'KH8513AK', 'ND', '5', 'Mobil Barang Bak Tertutup', 'C', 'TBLNG', 'A23', 'MT', '0', '2024-08-16 07:40:17', 'NOVITASARI', 'KH', '8513', 'AK', '', '', 'FE73', NULL, '0', 7000, NULL, '1', 'TBLNG', 'PLANK', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 2, 7.1, 1, '2024-11-01 15:48:36', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 1, 0, 1, '2024-11-14 14:37:27', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:04:17', 0, 104.009, 1, '2024-09-01 07:47:34', 0, 0, 0, '2024-09-24 02:42:53'),
(4, '0003', 'CB71C2351522', 'CB71C2351522', 'DA8119HH', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A12', 'MT', '0', '2024-08-16 07:43:24', 'HUSNA', 'HH', '8119', 'DA', NULL, NULL, 'TRITON DC-CR25', 330824, '0', 2850, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 1, 1.8, 1, '2024-11-01 15:48:53', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:04:17', 1, 100, 1, '2024-09-23 14:45:16', 0, 0, 0, '2024-09-24 02:42:53'),
(5, '0004', 'CB09C12002410', 'CB09C12002410', 'DA8165HD', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A11', 'SZ', '0', '2024-08-16 07:47:05', 'HUSNA', 'HD', '8165', 'DA', NULL, NULL, 'ST150', 332157, '1', 2085, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 0, NULL, NULL, '2024-11-01 14:38:40', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, 40.7, 1, '2024-11-15 15:12:49', 0, 61.6947, 1, '2024-09-01 09:25:37', 0, 0, 0, '2024-09-24 02:42:53'),
(6, '0005', 'CB09C23008656', 'CB09C23008656', 'DA8760HJ', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A12', 'MT', '0', '2024-08-16 08:00:49', 'HUSNA', 'DA', '8760', 'HJ', NULL, '', 'TRITON DC-CR25', 331965, '1', 2850, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 0, NULL, NULL, '2024-11-01 14:38:40', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 1, 60.7, 1, '2024-11-15 15:18:00', 2, 69.8675, 1, '2024-09-01 09:41:26', 0, 0, 0, '2024-09-24 02:42:53'),
(7, '0006', 'CB09C24008998', 'CB09C24008998', 'DA8253HH', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A12', 'MT', '0', '2024-08-16 08:04:38', 'HUSNA', 'DA', '8253', 'HH', NULL, NULL, 'TRITON DC-CR25', 332158, '1', 2850, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 0, NULL, NULL, '2024-11-01 14:38:40', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:04:17', 1, 101.778, 1, '2024-09-01 09:43:53', 0, 0, 0, '2024-09-24 02:42:53'),
(8, '0007', 'CB09C24009000', 'CB09C24009000', 'DA8327HH', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A12', 'MT', '0', '2024-08-16 08:22:24', 'HUSNA', 'DA', '8327', 'HH', NULL, NULL, 'TRITON DC-CR25', 332161, '1', 2850, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 0, NULL, NULL, '2024-11-01 14:38:40', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:04:17', 2, 56.6141, 1, '2024-09-01 08:06:12', 0, 0, 0, '2024-09-24 02:42:53'),
(9, '0008', 'CB09B15005407', 'CB09B15005407', 'DA7012HG', 'B', '2', 'Mobil Bus Sedang', 'B', 'TBLNG', 'B21', 'IZ', '0', '2024-08-16 08:33:22', 'HUSNA', 'HG', '7012', 'DA', NULL, NULL, 'NHR 55', 332056, '1', 5100, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 0, NULL, NULL, '2024-11-01 14:38:40', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:04:17', 2, 55.8998, 1, '2024-09-01 08:22:18', 0, 0, 0, '2024-09-24 02:42:53'),
(10, '0009', 'CB09B13003976', 'CB09B13003976', 'DA7319HB', 'B', '2', 'Mobil Bus Sedang', 'B', 'TBLNG', 'B21', 'MT', '0', '2024-08-16 08:34:24', 'HUSNA', 'HB', '7319', 'DA', NULL, NULL, 'BUS FE 74', 332053, '1', 7500, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 0, NULL, NULL, '2024-11-01 14:38:40', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:04:17', 2, 57.0848, 1, '2024-09-01 08:25:14', 0, 0, 0, '2024-09-24 02:42:53'),
(11, '0010', 'CB09C18006631', 'CB09C18006631', 'DA8032HC', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A12', 'MT', '0', '2024-08-16 08:35:14', 'HUSNA', 'HC', '8032', 'DA', NULL, NULL, 'TRITON DC-CR25', 332239, '1', 2730, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 0, NULL, NULL, '2024-11-01 14:38:40', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:04:17', 1, 104.238, 1, '2024-09-01 09:49:15', 0, 0, 0, '2024-09-24 02:42:53'),
(12, '0011', 'CB09C23008771', 'CB09C23008771', 'DA8803HJ', 'B', '2', 'Mobil Barang Bak Terbuka', 'C', 'TBLNG', 'A11', 'SZ', '0', '2024-08-16 08:38:32', 'HUSNA', 'DA', '8803', 'HJ', NULL, NULL, 'AEV415W CX 4X2 M/T', 332127, '1', 2190, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 0, NULL, NULL, '2024-11-01 14:38:40', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:04:17', 2, 74.864, 1, '2024-09-01 09:59:33', 0, 0, 0, '2024-09-24 02:42:53'),
(13, '0012', 'CB09B19007471', 'CB09B19007471', 'DA7568HB', 'B', '2', 'Mobil Bus Sedang', 'B', 'TBLNG', 'B21', 'IZ', '0', '2024-08-16 08:42:10', 'HUSNA', 'HB', '7568', 'DA', NULL, NULL, 'NLR 55B LX 4x2 M/T', 329006, '1', 5100, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 0, NULL, NULL, '2024-11-01 14:38:40', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:04:17', 1, 104.027, 1, '2024-09-01 10:03:08', 0, 0, 0, '2024-09-24 02:42:53'),
(14, '0013', 'CB09B18006930', 'CB09B18006930', 'DA7367HB', 'B', '2', 'Mobil Bus Sedang', 'B', 'TBLNG', 'B21', 'MT', '0', '2024-08-16 09:28:50', 'HUSNA', 'HB', '7367', 'DA', NULL, NULL, 'FE 84', 332139, '1', 8000, '1', '1', 'TBLNG', 'TBLNG', NULL, 0, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, 0, NULL, NULL, '2024-11-14 15:14:53', 0, NULL, NULL, '2024-11-01 14:46:51', 0, NULL, NULL, '2024-11-01 14:38:40', 0, NULL, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:02:20', 0, NULL, NULL, '2024-11-01 15:04:17', 1, 100.864, 1, '2024-09-01 10:19:45', 0, 0, 0, '2024-09-24 02:42:53');

-- --------------------------------------------------------

--
-- Table structure for table `tb_hlm`
--

CREATE TABLE `tb_hlm` (
  `id` int(11) NOT NULL,
  `hlm_value` float NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_hlm`
--

INSERT INTO `tb_hlm` (`id`, `hlm_value`) VALUES
(1, 40.7);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id_user` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `typex` smallint(6) NOT NULL DEFAULT 0 COMMENT '1=admin, 2=penguji, 3=operator loket 1, 4=operator loket 2, 5=operator loket 3',
  `type` smallint(6) NOT NULL COMMENT '1=admin, 2=operator',
  `nip` varchar(50) DEFAULT NULL,
  `image` varchar(50) DEFAULT 'free.jpg',
  `image_ttd` varchar(50) DEFAULT 'free.jpg',
  `sts` int(11) DEFAULT 1,
  `kode_cab` int(11) DEFAULT 0,
  `id_pegawai` int(11) NOT NULL DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id_user`, `nama`, `username`, `password`, `typex`, `type`, `nip`, `image`, `image_ttd`, `sts`, `kode_cab`, `id_pegawai`) VALUES
(42, 'PARJANTO, S.Sos', 'parjanto', '53d2732235a18d187f5f41a301e0cc1f', 2, 8, '063.009.PT3.01.001', 'parjanto.jpg', NULL, 1, 0, 42),
(70, 'CANDRA LUKITO, A.MA', 'lukito', 'cd40d10e7b45793a148bd7ddafdc18c6', 2, 8, '063.009.PT2.01.001', 'chandra.jpg', NULL, 1, 0, 40),
(79, 'DJATMIKO', 'miko', 'ef9322a1a342a36856e9e8929b19437a', 2, 8, '19691013 199403 1 010', 'miko.jpg', NULL, 1, 0, 38),
(1, 'Junaedi', 'junaedi', 'add3c3fed578a1c061379e86f14521ae', 4, 0, NULL, 'free.jpg', 'free.jpg', 1, 0, 0),
(2, 'Aldi', 'a', '$2y$10$7nkape1qHIpTRRuYhMmwYeHQLU9oT3YedLVcxR.UdqF', 0, 0, NULL, 'free.jpg', 'free.jpg', 1, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `web_sistem`
--

CREATE TABLE `web_sistem` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `logo` varchar(255) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `alamat` varchar(255) NOT NULL,
  `gambar_header` varchar(255) NOT NULL,
  `telp` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `instagram` varchar(255) DEFAULT NULL,
  `facebook` varchar(255) DEFAULT NULL,
  `twitter` varchar(255) DEFAULT NULL,
  `maps` text DEFAULT NULL,
  `id_user` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `web_sistem`
--

INSERT INTO `web_sistem` (`id`, `logo`, `nama`, `alamat`, `gambar_header`, `telp`, `email`, `instagram`, `facebook`, `twitter`, `maps`, `id_user`, `created_at`, `updated_at`) VALUES
(1, 'logo-header.png', 'Dinas Perhubungan Kabupaten Tabalong', 'Jl. Mabu’un Raya No. 39, Maburai, Murung Pudak, Maburai, Kec. Murung Pudak, Kabupaten Tabalong, Kalimantan Selatan 71571', '20220922204134.jpg', '1234567980', 'dishub@email.id', 'https://www.instagram.com/', 'https://www.facebook.com/', 'https://twitter.com/', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3986.936142915355!2d115.43098721526935!3d-2.1779483378642777!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dfab251f077a125%3A0xfc6d4a5257952f84!2sKantor%20Dinas%20Perhubungan%2C%20Komunikasi%20dan%20Informatika%20Kabupaten%20Tabalong!5e0!3m2!1sen!2sid!4v1665589571729!5m2!1sen!2sid', 1, '2022-08-05 12:40:19', '2022-10-12 14:47:43');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_cekident`
--
ALTER TABLE `tb_cekident`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tb_hlm`
--
ALTER TABLE `tb_hlm`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`);

--
-- Indexes for table `web_sistem`
--
ALTER TABLE `web_sistem`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_cekident`
--
ALTER TABLE `tb_cekident`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `tb_hlm`
--
ALTER TABLE `tb_hlm`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=80;

--
-- AUTO_INCREMENT for table `web_sistem`
--
ALTER TABLE `web_sistem`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
