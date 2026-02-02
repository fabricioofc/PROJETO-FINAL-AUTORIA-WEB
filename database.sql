-- =====================================================
-- Script de Criação e População do Banco de Dados
-- Desenvolvedores: Alec e Fabricio
-- O script cria o banco, as tabelas e insere todos os dados iniciais (categorias, autores e 10 posts).
-- =====================================================

-- Cria o banco de dados e o seleciona
CREATE DATABASE IF NOT EXISTS blog_db;
USE blog_db;

-- Tabela de Categorias
CREATE TABLE IF NOT EXISTS Categorias (
    ID_Categoria INT NOT NULL AUTO_INCREMENT,
    Nome VARCHAR(50) NOT NULL UNIQUE,
    Descricao TEXT,
    PRIMARY KEY (ID_Categoria)
);

-- Tabela de Autores
CREATE TABLE IF NOT EXISTS Autores (
    ID_Autor INT NOT NULL AUTO_INCREMENT,
    Nome VARCHAR(100) NOT NULL,
    Email VARCHAR(150) NOT NULL,
    Bio TEXT,
    PRIMARY KEY (ID_Autor),
    UNIQUE KEY uk_autor_email (Email)
);

-- Tabela de Posts
CREATE TABLE IF NOT EXISTS Posts (
    ID_Post INT NOT NULL AUTO_INCREMENT,
    Titulo VARCHAR(200) NOT NULL,
    Slug VARCHAR(200) NOT NULL UNIQUE,
    Conteudo TEXT NOT NULL,
    ID_Categoria INT,
    ID_Autor INT,
    Data_Publicacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    Visualizacoes INT DEFAULT 0,
    Status VARCHAR(20) DEFAULT 'Rascunho',
    Imagem VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (ID_Post),
    FOREIGN KEY (ID_Categoria) REFERENCES Categorias(ID_Categoria) ON DELETE SET NULL,
    CONSTRAINT fk_post_autor 
        FOREIGN KEY (ID_Autor) REFERENCES Autores (ID_Autor) 
        ON UPDATE CASCADE 
        ON DELETE SET NULL,
    CHECK (Status IN ('Rascunho', 'Publicado', 'Arquivado')),
    FULLTEXT INDEX ft_titulo_conteudo (Titulo, Conteudo),
    KEY idx_post_autor (ID_Autor),
    INDEX idx_data (Data_Publicacao),
    INDEX idx_categoria_data (ID_Categoria, Data_Publicacao),
    INDEX idx_status (Status)
);

-- Inserção de Categorias Iniciais
INSERT INTO Categorias (Nome, Descricao) VALUES
('Inovação', 'Artigos sobre novas tecnologias e tendências disruptivas'), -- ID 1
('Empreendedorismo Digital', 'Estratégias para negócios no mundo online'), -- ID 2
('Gestão de Negócios', 'Dicas e metodologias para administrar empresas'), -- ID 3
('Liderança', 'Desenvolvimento de competências para líderes modernos'), -- ID 4
('Marketing', 'Estratégias de conteúdo e atração de clientes'), -- ID 5
('Finanças', 'Planejamento e controle financeiro para empreendedores'), -- ID 6
('Cultura Organizacional', 'Gestão de pessoas e ambiente de trabalho'), -- ID 7
('Sustentabilidade', 'Práticas de ESG e impacto socioambiental nos negócios'); -- ID 8

-- Inserção de Autores Iniciais
INSERT INTO Autores (Nome, Email, Bio) VALUES
('Alec', 'alec@ifrn.edu.br', 'Estudante de Informática no IFRN'), -- ID 1
('Fabricio', 'fabricio@ifrn.edu.br', 'Estudante de Informática no IFRN'); -- ID 2

-- Inserção dos 10 Posts Iniciais (5 para cada autor)
-- Posts do Autor Alec (ID 1)
INSERT INTO Posts (Titulo, Slug, Conteudo, ID_Categoria, ID_Autor, Status, Imagem) VALUES
('Tendências de Inovação para Pequenas Empresas em 2026', 'tendencias-inovacao-pme-2026', 'A inovação não é um luxo reservado apenas às grandes corporações. Para as pequenas e médias empresas (PMEs), ela é a espinha dorsal da sobrevivência e do crescimento em um mercado cada vez mais dinâmico. Em 2026, algumas tendências se destacam como cruciais para as PMEs que buscam se manter competitivas.', 1, 1, 'Publicado', 'post1.jpg'),
('Como o Empreendedorismo Digital está Transformando o Mercado', 'empreendedorismo-digital-transformacao', 'O Empreendedorismo Digital não é apenas sobre vender online; é uma mudança fundamental na forma como os negócios são concebidos, lançados e escalados. Ele se baseia na criação de valor através de produtos e serviços digitais ou na digitalização de modelos de negócios tradicionais.', 2, 1, 'Publicado', 'post2.jpg'),
('Estratégias de Gestão de Negócios para Crescimento Sustentável', 'gestao-negocios-crescimento-sustentavel', 'Crescer rapidamente é o sonho de todo empreendedor, mas o crescimento sustentável é o que garante a longevidade do negócio. Uma gestão focada na sustentabilidade não se limita ao aspecto ambiental, mas abrange a saúde financeira, a estabilidade operacional e o bem-estar dos colaboradores.', 3, 1, 'Publicado', 'post3.jpg'),
('O Papel da Inteligência Artificial na Inovação Empresarial', 'ia-inovacao-empresarial', 'A Inteligência Artificial (IA) deixou de ser uma promessa futurista para se tornar uma ferramenta de inovação acessível a empresas de todos os portes. Seu papel na inovação empresarial é multifacetado, atuando desde a otimização de rotinas até a criação de novos produtos.', 1, 1, 'Publicado', 'post4.jpg'),
('Liderança Moderna: Como Inspirar Equipes em Tempos de Mudança', 'lideranca-moderna-inspiracao', 'Em um mundo de negócios caracterizado pela volatilidade, incerteza, complexidade e ambiguidade (VUCA), o modelo de liderança tradicional, baseado em comando e controle, está obsoleto. A Liderança Moderna é, acima de tudo, inspiradora e adaptável.', 4, 1, 'Publicado', 'post5.jpg');

-- Posts do Autor Fabricio (ID 2)
INSERT INTO Posts (Titulo, Slug, Conteudo, ID_Categoria, ID_Autor, Status, Imagem) VALUES
('Marketing de Conteúdo: A Chave para Atrair Clientes no Mundo Digital', 'marketing-conteudo-atrair-clientes', 'No cenário digital saturado de anúncios, o Marketing de Conteúdo se estabeleceu como a estratégia mais eficaz para atrair, engajar e converter clientes. Em vez de interromper o público com publicidade, ele se concentra em entregar valor por meio de informações relevantes e úteis.', 5, 2, 'Publicado', 'post6.jpg'),
('Planejamento Financeiro para Novos Empreendedores', 'planejamento-financeiro-novos-empreendedores', 'O Planejamento Financeiro é o mapa que guia o novo empreendedor através das incertezas iniciais. Começar um negócio sem um plano financeiro sólido é como navegar sem bússola: o fracasso é quase inevitável.', 6, 2, 'Publicado', 'post7.jpg'),
('A Importância da Cultura Organizacional na Retenção de Talentos', 'cultura-organizacional-retencao-talentos', 'Em um mercado de trabalho competitivo, o salário não é mais o único fator de atração e retenção. A Cultura Organizacional ‒ o conjunto de valores, crenças e práticas que moldam o comportamento na empresa ‒ tornou-se o principal diferencial.', 7, 2, 'Publicado', 'post8.jpg'),
('Networking: Como Construir Parcerias Estratégicas de Sucesso', 'networking-parcerias-estrategicas', 'No mundo dos negócios, ninguém cresce sozinho. O Networking eficaz é a arte de construir e manter uma rede de relacionamentos que pode gerar oportunidades, conhecimento e apoio mútuo.', 3, 2, 'Publicado', 'post9.jpg'),
('Sustentabilidade como Diferencial Competitivo nos Negócios', 'sustentabilidade-diferencial-competitivo', 'A sustentabilidade deixou de ser uma preocupação puramente ética para se tornar um diferencial competitivo estratégico. Empresas que adotam práticas sustentáveis não apenas reduzem riscos e custos, mas também atraem uma nova geração de consumidores conscientes.', 8, 2, 'Publicado', 'post10.jpg');
