CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS locais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    responsavel TEXT,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS bens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    descricao TEXT,
    categoria_id INTEGER REFERENCES categorias(id) ON DELETE RESTRICT,
    local_id INTEGER REFERENCES locais(id) ON DELETE RESTRICT,
    status TEXT NOT NULL DEFAULT 'Ativo',
    valor REAL NOT NULL DEFAULT 0,
    data_aquisicao TEXT,
    criado_em TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bem_id INTEGER NOT NULL REFERENCES bens(id) ON DELETE CASCADE,
    local_origem_id INTEGER REFERENCES locais(id) ON DELETE SET NULL,
    local_destino_id INTEGER REFERENCES locais(id) ON DELETE SET NULL,
    data TEXT NOT NULL,
    observacao TEXT
);

INSERT OR IGNORE INTO categorias (nome, descricao) VALUES
    ('Informática', 'Computadores, notebooks, monitores e periféricos'),
    ('Mobiliário', 'Mesas, cadeiras, armários e estantes'),
    ('Eletrônicos', 'Projetores, televisores e equipamentos de áudio'),
    ('Veículos', 'Veículos e equipamentos de transporte');

INSERT OR IGNORE INTO locais (nome, responsavel, descricao) VALUES
    ('Secretaria', 'Coordenação administrativa', 'Sala da secretaria'),
    ('Laboratório de Informática', 'Suporte técnico', 'Laboratório de aulas práticas'),
    ('Sala de Reuniões', 'Direção', 'Sala para reuniões e atendimentos');
