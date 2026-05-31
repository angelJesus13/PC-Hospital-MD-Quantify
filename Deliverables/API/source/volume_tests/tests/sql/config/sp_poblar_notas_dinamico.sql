DELIMITER $$
CREATE PROCEDURE sp_poblar_notas_dinamico(
    IN p_cantidad INT,
    IN p_tipos_nota VARCHAR(255),
    IN p_pediatria BOOLEAN,
    IN p_uci BOOLEAN,
    IN p_zero BOOLEAN,
    IN p_usuario_ip VARCHAR(100)
)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE v_edad INT;
    DECLARE v_genero VARCHAR(15);
    DECLARE v_es_zero BOOLEAN;
    
    DECLARE v_estatus BIT(1) DEFAULT b'1';
    DECLARE v_tipo_nota VARCHAR(50);
    DECLARE v_antecedentes TEXT;
    DECLARE v_sintomas TEXT;
    DECLARE v_interrogatorio TEXT;
    DECLARE v_signos VARCHAR(255);
    DECLARE v_paciente_id INT;
    DECLARE v_medico_id INT;
    DECLARE v_expediente_id INT;
    DECLARE v_fecha_reg DATETIME;
    
    -- Variables para parsear CSV
    DECLARE num_tipos INT;
    DECLARE eleccion INT;
    
    IF p_cantidad IS NULL OR p_cantidad <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: la cantidad debe ser mayor a 0.';
    END IF;

    SET num_tipos = LENGTH(p_tipos_nota) - LENGTH(REPLACE(p_tipos_nota, ',', '')) + 1;

    WHILE i < p_cantidad DO
        -- Escoger orgánicamente un "TipoNota" estricto del JSON array inyectado por python
        SET eleccion = FLOOR(1 + RAND() * num_tipos);
        SET v_tipo_nota = SUBSTRING_INDEX(SUBSTRING_INDEX(p_tipos_nota, ',', eleccion), ',', -1);
        
        IF p_zero THEN
            SET v_es_zero = TRUE;
        ELSE
            SET v_es_zero = FALSE; 
        END IF;

        -- Asegurar ID's reales para las llaves foráneas esenciales
        SET v_medico_id = FLOOR(1 + RAND() * 49); -- Medico aleatorio del 1 al 50 garantizado
        SET v_paciente_id = FLOOR(1 + RAND() * 149); -- Paciente aleatorio del 1 al 150 garantizado
        SET v_expediente_id = v_paciente_id; -- Expediente referenciado exactamente al mismo ID de paciente
        
        IF p_pediatria THEN
            SET v_edad = FLOOR(1 + RAND() * 14);
        ELSE
            SET v_edad = FLOOR(18 + RAND() * 60);
        END IF;
        
        IF RAND() < 0.5 THEN SET v_genero = 'hombre'; ELSE SET v_genero = 'mujer'; END IF;
        SET v_fecha_reg = DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 365) DAY);
        
        SET v_antecedentes = fn_generar_antecedentes(v_es_zero);
        
        IF p_uci THEN
            SET v_sintomas = fn_generar_sintomas(TRUE);
            SET v_signos = fn_generar_signos_vitales(TRUE, 'critico');
        ELSEIF v_tipo_nota = 'Urgencia' THEN
            SET v_sintomas = fn_generar_sintomas(v_es_zero);
            SET v_signos = fn_generar_signos_vitales(v_es_zero, 'urgencia');
        ELSE
            SET v_sintomas = fn_generar_sintomas(v_es_zero);
            SET v_signos = fn_generar_signos_vitales(v_es_zero, 'general');
        END IF;
        
        SET v_interrogatorio = fn_generar_interrogatorio(v_es_zero, v_genero, v_edad);

        INSERT INTO tbb_md_notas_medicas (
            FechaRegistro, Estatus, TipoNota, AntecedentesRelevantes, 
            SintomasActuales, InterrogatorioAnamnesis, SignosVitales,
            Auditoria, Paciente_ID, Medico_ID, Expediente_ID
        ) VALUES (
            v_fecha_reg, v_estatus, v_tipo_nota, v_antecedentes,
            v_sintomas, v_interrogatorio, v_signos, fn_generar_auditoria(''), v_paciente_id,
            v_medico_id, v_expediente_id
        );
        
        IF i > 0 AND i % 5000 = 0 THEN
            COMMIT;
        END IF;
        
        SET i = i + 1;
    END WHILE;
    
    COMMIT;
    
    -- Bitácora para el test especifico
    INSERT INTO tbi_bitacora (NombreTabla, Operacion, Descripcion, usuario)
    VALUES (
        'tbb_md_notas_medicas', 
        'INSERT Pydantic', 
        CONCAT('Configuración API: ', p_cantidad, ' registros generados. Tipos: [', p_tipos_nota, ']. Pediatria/UCI/Zero: ', p_pediatria, '/', p_uci, '/', p_zero), 
        p_usuario_ip
    );
    
    COMMIT;
END$$
DELIMITER ;
