-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : db
-- Généré le : jeu. 11 jan. 2024 à 21:50
-- Version du serveur : 8.2.0
-- Version de PHP : 8.2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `OGPT`
--

-- --------------------------------------------------------

--
-- Structure de la table `Form`
--

CREATE TABLE `Form` (
  `id` int NOT NULL,
  `userId` int NOT NULL,
  `nbEntreprise` int NOT NULL,
  `nbReponse` int NOT NULL,
  `nbEntretien` int NOT NULL,
  `validate` tinyint(1) DEFAULT '2'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Grade`
--

CREATE TABLE `Grade` (
  `id` int NOT NULL,
  `userId` int NOT NULL,
  `IA` int NOT NULL,
  `Systeme` int NOT NULL,
  `BDD` int NOT NULL,
  `Stage` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `User`
--

CREATE TABLE `User` (
  `id` int NOT NULL,
  `Type` enum('Admin','Etudiant') NOT NULL,
  `FirstName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` varchar(200) NOT NULL,
  `UserList_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `User`
--

INSERT INTO `User` (`id`, `Type`, `FirstName`, `LastName`, `username`, `password`, `UserList_id`) VALUES
(13, 'Admin', 'Admin', 'Admin', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `UserList`
--

CREATE TABLE `UserList` (
  `id` int NOT NULL,
  `promo` enum('B1','B2') NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Form`
--
ALTER TABLE `Form`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `userId` (`userId`),
  ADD KEY `Form_FK_1` (`userId`);

--
-- Index pour la table `Grade`
--
ALTER TABLE `Grade`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `userId` (`userId`),
  ADD KEY `grade_FK_1` (`userId`);

--
-- Index pour la table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `User_FK_1` (`UserList_id`);

--
-- Index pour la table `UserList`
--
ALTER TABLE `UserList`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Form`
--
ALTER TABLE `Form`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Grade`
--
ALTER TABLE `Grade`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `User`
--
ALTER TABLE `User`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT pour la table `UserList`
--
ALTER TABLE `UserList`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `Form`
--
ALTER TABLE `Form`
  ADD CONSTRAINT `Form_FK_1` FOREIGN KEY (`userId`) REFERENCES `User` (`id`);

--
-- Contraintes pour la table `Grade`
--
ALTER TABLE `Grade`
  ADD CONSTRAINT `grade_FK_1` FOREIGN KEY (`userId`) REFERENCES `User` (`id`);

--
-- Contraintes pour la table `User`
--
ALTER TABLE `User`
  ADD CONSTRAINT `User_FK_1` FOREIGN KEY (`UserList_id`) REFERENCES `UserList` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
