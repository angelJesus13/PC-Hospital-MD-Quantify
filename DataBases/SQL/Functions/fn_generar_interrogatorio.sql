DELIMITER $$
CREATE FUNCTION fn_generar_interrogatorio(p_es_paciente_zero BOOLEAN, p_genero VARCHAR(15), p_edad INT)
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE v_tiempo VARCHAR(50);
    DECLARE v_estado VARCHAR(100);
    
    IF p_es_paciente_zero = TRUE THEN
        RETURN 'PACIENTE ZERO. Ingresa en calidad de desconocido. No es posible recabar interrogatorio directo por estado de inconsciencia ni indirecto por ausencia de familiares. Abordaje emergente.';
    END IF;
    
    SET v_tiempo = ELT(FLOOR(1 + RAND() * 6),
        'pocas horas', 'esta misma mañana', 'la noche anterior', 'hace 3 días', 'hace una semana', 'de forma gradual');
        
    SET v_estado = ELT(FLOOR(1 + RAND() * 5),
        'Paciente acude consciente y orientado en sus 3 esferas.',
        'Acude con facies de dolor intenso y marcha claudicante.',
        'Se observa hemodinámicamente estable pero refiriendo molestia persistente.',
        'Ingresa acompañado de familiar refiriendo deterioro del estado general.',
        'Acude ansioso/a solicitando atención médica inmediata en triaje.');
        
    RETURN CONCAT('Paciente ', LOWER(IFNULL(p_genero, 'de género no especificado')), ' de ', IFNULL(p_edad, 0), 
                  ' años. Inicia su padecimiento actual ', v_tiempo, '. ', v_estado);
END$$
DELIMITER ;
