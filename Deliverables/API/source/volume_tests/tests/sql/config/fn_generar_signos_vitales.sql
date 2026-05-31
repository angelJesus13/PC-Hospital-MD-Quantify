DELIMITER $$
CREATE FUNCTION fn_generar_signos_vitales(p_es_paciente_zero BOOLEAN, p_escenario VARCHAR(30))
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    DECLARE v_rand FLOAT;
    IF p_es_paciente_zero = TRUE THEN
        RETURN 'No recabados';
    END IF;
    
    SET v_rand = RAND();
    IF p_escenario = 'uci' OR p_escenario = 'critico' THEN
        RETURN 'FC:130 lpm, FR:28 rpm, TA:160/100 mmHg, Temp:39.0°C, SpO2:88%'; -- Crítico
    ELSEIF p_escenario = 'urgencia' THEN
        RETURN 'FC:110 lpm, FR:24 rpm, TA:140/90 mmHg, Temp:38.5°C, SpO2:92%'; -- Alterado
    ELSE
        -- Normal o Leve (General)
        IF v_rand < 0.5 THEN
            RETURN 'FC:80 lpm, FR:16 rpm, TA:120/80 mmHg, Temp:36.5°C, SpO2:98%';
        ELSEIF v_rand < 0.8 THEN
            RETURN 'FC:95 lpm, FR:20 rpm, TA:130/85 mmHg, Temp:37.2°C, SpO2:96%';
        ELSE
            RETURN 'FC:60 lpm, FR:14 rpm, TA:100/60 mmHg, Temp:36.0°C, SpO2:95%';
        END IF;
    END IF;
END$$
DELIMITER ;
