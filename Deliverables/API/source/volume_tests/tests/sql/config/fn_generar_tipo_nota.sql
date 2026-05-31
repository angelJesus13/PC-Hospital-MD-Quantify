DELIMITER $$
CREATE FUNCTION fn_generar_tipo_nota()
RETURNS VARCHAR(50)
DETERMINISTIC
BEGIN
    DECLARE v_rand FLOAT;
    DECLARE v_tipo VARCHAR(50);
    SET v_rand = RAND();
    
    IF v_rand < 0.10 THEN SET v_tipo = 'Ingreso';
    ELSEIF v_rand < 0.45 THEN SET v_tipo = 'Evolución';
    ELSEIF v_rand < 0.65 THEN SET v_tipo = 'Urgencia';
    ELSEIF v_rand < 0.80 THEN SET v_tipo = 'Interconsulta';
    ELSE SET v_tipo = 'Egreso';
    END IF;
    
    RETURN v_tipo;
END$$
DELIMITER ;
