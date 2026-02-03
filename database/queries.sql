-- DDL para criação da tabela
CREATE TABLE despesas_ans (
    cnpj VARCHAR(14),
    razao_social VARCHAR(255),
    uf VARCHAR(2),
    ano INT,
    trimestre INT,
    valor DECIMAL(18,2)
);

-- Pergunta 1: Crescimento Percentual T1 vs T3 em 2023
WITH Dados2023 AS (
    SELECT 
        razao_social,
        SUM(CASE WHEN trimestre = 1 THEN valor ELSE 0 END) as v1,
        SUM(CASE WHEN trimestre = 3 THEN valor ELSE 0 END) as v3
    FROM despesas_ans
    WHERE ano = 2023
    GROUP BY razao_social
)
SELECT 
    razao_social,
    v1 as valor_t1,
    v3 as valor_t3,
    ROUND(((v3 - v1) / NULLIF(v1, 0)) * 100, 2) as crescimento_percentual
FROM Dados2023
WHERE v1 > 0
ORDER BY crescimento_percentual DESC;

-- Pergunta 2: Média de despesas por UF
SELECT 
    uf, 
    ROUND(AVG(valor), 2) as media_valor
FROM despesas_ans
GROUP BY uf
ORDER BY media_valor DESC;