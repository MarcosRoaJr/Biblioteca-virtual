-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Tempo de geração: 24/08/2025 às 02:05
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `biblioteca_virtual`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `autor`
--

CREATE TABLE `autor` (
  `id_autor` int(11) NOT NULL,
  `nome` varchar(80) NOT NULL,
  `sobrenome` varchar(120) NOT NULL,
  `nome_completo` varchar(200) GENERATED ALWAYS AS (concat(`nome`,' ',`sobrenome`)) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `editora`
--

CREATE TABLE `editora` (
  `id_editora` int(11) NOT NULL,
  `Nome` varchar(180) NOT NULL,
  `Telefone` varchar(16) NOT NULL,
  `Endereço` varchar(70) NOT NULL,
  `Bairro` varchar(80) NOT NULL,
  `Cidade` varchar(100) NOT NULL,
  `Cep` varchar(9) NOT NULL,
  `CNPJ` varchar(18) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `emprestimo`
--

CREATE TABLE `emprestimo` (
  `id_emprestimo` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `status_emprestimo` enum('Emprestado','Perdido','Atrasado','Cancelado','Devolvido') NOT NULL DEFAULT 'Emprestado',
  `data_saida` date NOT NULL,
  `hora_saida` time(6) NOT NULL,
  `data_prevista_devolucao` date NOT NULL,
  `data_devolucao` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `exemplares`
--

CREATE TABLE `exemplares` (
  `numero_patrimonio` int(11) NOT NULL,
  `id_livro` int(11) NOT NULL,
  `codigo_barras` varchar(25) NOT NULL,
  `valor_livro` decimal(10,2) NOT NULL,
  `data_compra` date NOT NULL,
  `usuario_comprador` varchar(120) NOT NULL,
  `etiqueta` varchar(10) NOT NULL,
  `numero_exemplar` int(10) NOT NULL,
  `status` enum('Disponível','Emprestado','Perdido','Cancelado','Danificado','Manutenção') NOT NULL DEFAULT 'Disponível'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `genero`
--

CREATE TABLE `genero` (
  `id_genero` int(11) NOT NULL,
  `genero` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `livro`
--

CREATE TABLE `livro` (
  `id_livro` int(11) NOT NULL,
  `id_editora` int(11) NOT NULL,
  `ISBN` varchar(20) NOT NULL,
  `local_posicao` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `data_publicacao` date NOT NULL,
  `data_entrada` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `livro_autor`
--

CREATE TABLE `livro_autor` (
  `id_livroautor` int(11) NOT NULL,
  `id_livro` int(11) NOT NULL,
  `id_autor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `livro_emprestimo`
--

CREATE TABLE `livro_emprestimo` (
  `id_emprestimo` int(11) NOT NULL,
  `id_numero_patrimonio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `livro_genero`
--

CREATE TABLE `livro_genero` (
  `id_generolivro` int(11) NOT NULL,
  `id_genero` int(11) NOT NULL,
  `id_livro` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `localidade_livro`
--

CREATE TABLE `localidade_livro` (
  `id_campus` int(11) NOT NULL,
  `nome` varchar(180) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `posicao_livro`
--

CREATE TABLE `posicao_livro` (
  `id_local_geral` int(11) NOT NULL,
  `setor` varchar(180) NOT NULL,
  `estante` varchar(80) NOT NULL,
  `id_campus` int(11) NOT NULL,
  `id_local` int(11) GENERATED ALWAYS AS (concat(`setor`,`estante`,'-',`id_campus`)) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nome` varchar(120) NOT NULL,
  `data_nascimento` date NOT NULL,
  `email` varchar(320) NOT NULL,
  `cpf` varchar(14) NOT NULL,
  `telefone` varchar(15) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `nivel_acesso` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `autor`
--
ALTER TABLE `autor`
  ADD PRIMARY KEY (`id_autor`);

--
-- Índices de tabela `editora`
--
ALTER TABLE `editora`
  ADD PRIMARY KEY (`id_editora`);

--
-- Índices de tabela `emprestimo`
--
ALTER TABLE `emprestimo`
  ADD PRIMARY KEY (`id_emprestimo`),
  ADD KEY `idx_usuario` (`id_usuario`);

--
-- Índices de tabela `exemplares`
--
ALTER TABLE `exemplares`
  ADD PRIMARY KEY (`numero_patrimonio`),
  ADD UNIQUE KEY `uk_numero_exemplar_por_livro` (`id_livro`,`numero_exemplar`);

--
-- Índices de tabela `genero`
--
ALTER TABLE `genero`
  ADD PRIMARY KEY (`id_genero`);

--
-- Índices de tabela `livro`
--
ALTER TABLE `livro`
  ADD PRIMARY KEY (`id_livro`),
  ADD UNIQUE KEY `uk_livro_isbn` (`ISBN`),
  ADD KEY `id_editora` (`id_editora`),
  ADD KEY `local_posicao` (`local_posicao`);

--
-- Índices de tabela `livro_autor`
--
ALTER TABLE `livro_autor`
  ADD PRIMARY KEY (`id_livroautor`),
  ADD KEY `fk_la_autor` (`id_autor`),
  ADD KEY `fk_la_livro` (`id_livro`);

--
-- Índices de tabela `livro_emprestimo`
--
ALTER TABLE `livro_emprestimo`
  ADD KEY `livro_emprestimo_ibfk_1` (`id_numero_patrimonio`),
  ADD KEY `id_emprestimo` (`id_emprestimo`);

--
-- Índices de tabela `livro_genero`
--
ALTER TABLE `livro_genero`
  ADD PRIMARY KEY (`id_generolivro`),
  ADD KEY `fk_lg_genero` (`id_genero`),
  ADD KEY `fk_lg_livro` (`id_livro`);

--
-- Índices de tabela `localidade_livro`
--
ALTER TABLE `localidade_livro`
  ADD PRIMARY KEY (`id_campus`);

--
-- Índices de tabela `posicao_livro`
--
ALTER TABLE `posicao_livro`
  ADD PRIMARY KEY (`id_local_geral`),
  ADD KEY `id_campus` (`id_campus`);

--
-- Índices de tabela `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `autor`
--
ALTER TABLE `autor`
  MODIFY `id_autor` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `editora`
--
ALTER TABLE `editora`
  MODIFY `id_editora` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `emprestimo`
--
ALTER TABLE `emprestimo`
  MODIFY `id_emprestimo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `exemplares`
--
ALTER TABLE `exemplares`
  MODIFY `numero_patrimonio` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `genero`
--
ALTER TABLE `genero`
  MODIFY `id_genero` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `livro`
--
ALTER TABLE `livro`
  MODIFY `id_livro` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `livro_autor`
--
ALTER TABLE `livro_autor`
  MODIFY `id_livroautor` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `livro_genero`
--
ALTER TABLE `livro_genero`
  MODIFY `id_generolivro` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `localidade_livro`
--
ALTER TABLE `localidade_livro`
  MODIFY `id_campus` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `posicao_livro`
--
ALTER TABLE `posicao_livro`
  MODIFY `id_local_geral` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `emprestimo`
--
ALTER TABLE `emprestimo`
  ADD CONSTRAINT `emprestimo_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);

--
-- Restrições para tabelas `exemplares`
--
ALTER TABLE `exemplares`
  ADD CONSTRAINT `fk_exemplares_livro` FOREIGN KEY (`id_livro`) REFERENCES `livro` (`id_livro`) ON DELETE CASCADE;

--
-- Restrições para tabelas `livro`
--
ALTER TABLE `livro`
  ADD CONSTRAINT `livro_ibfk_1` FOREIGN KEY (`id_editora`) REFERENCES `editora` (`id_editora`),
  ADD CONSTRAINT `livro_ibfk_2` FOREIGN KEY (`local_posicao`) REFERENCES `posicao_livro` (`id_local_geral`);

--
-- Restrições para tabelas `livro_autor`
--
ALTER TABLE `livro_autor`
  ADD CONSTRAINT `fk_la_autor` FOREIGN KEY (`id_autor`) REFERENCES `autor` (`id_autor`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_la_livro` FOREIGN KEY (`id_livro`) REFERENCES `livro` (`id_livro`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `livro_emprestimo`
--
ALTER TABLE `livro_emprestimo`
  ADD CONSTRAINT `livro_emprestimo_ibfk_1` FOREIGN KEY (`id_numero_patrimonio`) REFERENCES `exemplares` (`numero_patrimonio`),
  ADD CONSTRAINT `livro_emprestimo_ibfk_2` FOREIGN KEY (`id_emprestimo`) REFERENCES `emprestimo` (`id_emprestimo`);

--
-- Restrições para tabelas `livro_genero`
--
ALTER TABLE `livro_genero`
  ADD CONSTRAINT `fk_lg_genero` FOREIGN KEY (`id_genero`) REFERENCES `genero` (`id_genero`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_lg_livro` FOREIGN KEY (`id_livro`) REFERENCES `livro` (`id_livro`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `posicao_livro`
--
ALTER TABLE `posicao_livro`
  ADD CONSTRAINT `posicao_livro_ibfk_1` FOREIGN KEY (`id_campus`) REFERENCES `localidade_livro` (`id_campus`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
