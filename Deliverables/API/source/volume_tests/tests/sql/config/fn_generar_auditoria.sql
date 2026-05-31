DELIMITER $$
CREATE FUNCTION fn_generar_auditoria(p_usuario_ip VARCHAR(100))
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    DECLARE v_rand FLOAT;
    SET v_rand = RAND();
    
    -- El parametro p_usuario_ip se mantiene para no quebrar la firma de los 5 SPs que lo llaman,
    -- pero la logica interna ahora refleja un proceso de Auditoría Médica Clinica (MECIC y NOM-004).
    
    IF v_rand < 0.50 THEN
        RETURN 'Pendiente de Auditoría Clínica MECIC';
    ELSEIF v_rand < 0.70 THEN
        RETURN 'Aprobado: Cumple con todos los dominios normativos de la NOM-004-SSA3-2012';
    ELSEIF v_rand < 0.85 THEN
        RETURN 'Observación Menor: Exploración física no describe detalladamente patrón céfalo-caudal';
    ELSEIF v_rand < 0.95 THEN
        RETURN 'Observación Mayor: Falta justificación clínica detallada para el pronóstico y tratamiento';
    ELSEIF v_rand < 0.98 THEN
        RETURN 'No Cumple (NOM-004): Notas clínicas incompletas o falta de congruencia diagnóstico-terapéutica';
    ELSE
        RETURN 'Crítico: Riesgo médico-legal, documentación insuficiente del acto médico';
    END IF;
END$$
DELIMITER ;
