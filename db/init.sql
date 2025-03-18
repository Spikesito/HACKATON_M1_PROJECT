-- Création de la base de données et de l'utilisateur
DO $$ 
BEGIN 
   IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'kdd_cup99') THEN 
      CREATE DATABASE kdd_cup99;
   END IF;
END $$;

-- Connexion à la base de données
\c kdd_cup99;

-- Création de la table network_logs avec toutes les colonnes du CSV
CREATE TABLE IF NOT EXISTS network_logs (
    id SERIAL PRIMARY KEY,
    duration INTEGER,
    protocol_type VARCHAR(10),
    service VARCHAR(20),
    flag VARCHAR(10),
    src_bytes INTEGER,
    dst_bytes INTEGER,
    land INTEGER,
    wrong_fragment INTEGER,
    urgent INTEGER,
    hot INTEGER,
    num_failed_logins INTEGER,
    logged_in INTEGER,
    lnum_compromised INTEGER,
    lroot_shell INTEGER,
    lsu_attempted INTEGER,
    lnum_root INTEGER,
    lnum_file_creations INTEGER,
    lnum_shells INTEGER,
    lnum_access_files INTEGER,
    lnum_outbound_cmds INTEGER,
    is_host_login INTEGER,
    is_guest_login INTEGER,
    count INTEGER,
    srv_count INTEGER,
    serror_rate FLOAT,
    srv_serror_rate FLOAT,
    rerror_rate FLOAT,
    srv_rerror_rate FLOAT,
    same_srv_rate FLOAT,
    diff_srv_rate FLOAT,
    srv_diff_host_rate FLOAT,
    dst_host_count INTEGER,
    dst_host_srv_count INTEGER,
    dst_host_same_srv_rate FLOAT,
    dst_host_diff_srv_rate FLOAT,
    dst_host_same_src_port_rate FLOAT,
    dst_host_srv_diff_host_rate FLOAT,
    dst_host_serror_rate FLOAT,
    dst_host_srv_serror_rate FLOAT,
    dst_host_rerror_rate FLOAT,
    dst_host_srv_rerror_rate FLOAT,
    label VARCHAR(50)
);

-- Importation des données depuis le fichier CSV
COPY network_logs(duration, protocol_type, service, flag, src_bytes, dst_bytes, land, wrong_fragment, urgent, hot, 
                  num_failed_logins, logged_in, lnum_compromised, lroot_shell, lsu_attempted, lnum_root, 
                  lnum_file_creations, lnum_shells, lnum_access_files, lnum_outbound_cmds, is_host_login, 
                  is_guest_login, count, srv_count, serror_rate, srv_serror_rate, rerror_rate, srv_rerror_rate, 
                  same_srv_rate, diff_srv_rate, srv_diff_host_rate, dst_host_count, dst_host_srv_count, 
                  dst_host_same_srv_rate, dst_host_diff_srv_rate, dst_host_same_src_port_rate, dst_host_srv_diff_host_rate, 
                  dst_host_serror_rate, dst_host_srv_serror_rate, dst_host_rerror_rate, dst_host_srv_rerror_rate, label)
FROM '/docker-entrypoint-initdb.d/KDDCup99.csv'
DELIMITER ',' CSV HEADER;