DELIMITER $$
CREATE FUNCTION fn_generar_antecedentes(p_es_paciente_zero BOOLEAN)
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE v_rand FLOAT;
    DECLARE v_cronica VARCHAR(100);
    DECLARE v_alergias VARCHAR(100);
    DECLARE v_cx VARCHAR(100);
    
    IF p_es_paciente_zero = TRUE THEN
        RETURN NULL;
    END IF;
    
    SET v_rand = RAND();
    IF v_rand < 0.40 THEN
        RETURN NULL; -- 40% pacientes sin antecedentes relevantes reportados al ingresar nota
    END IF;
    
    SET v_cronica = ELT(FLOOR(1 + RAND() * 8),
        'Sin comorbilidades', 'Hipertensión Arterial Sistémica (HAS) controlada', 
        'Diabetes Mellitus Tipo 2 (DM2) en manejo', 'HAS + DM2 de 10 años de diagnóstico',
        'Hipotiroidismo', 'Asma bronquial intermitente', 
        'Tabaquismo intenso (IT>20)', 'Alcoholismo social');
        
    SET v_alergias = ELT(FLOOR(1 + RAND() * 5),
        'Sin alergias medicamentosas', 'Alérgico a Penicilina', 
        'Alérgico a AINEs', 'Alérgico a Sulfamidas', 'Alergia alimentaria (Mariscos)');
        
    SET v_cx = ELT(FLOOR(1 + RAND() * 5),
        'Sin cirugías previas', 'Colecistectomía', 'Apendicectomía', 'Cesárea', 'Amigdalectomía');
        
    RETURN CONCAT('Crónicos: ', v_cronica, ' | Alergias: ', v_alergias, ' | Cx previas: ', v_cx);
END$$
DELIMITER ;
