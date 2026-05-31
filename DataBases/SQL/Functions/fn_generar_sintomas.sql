DELIMITER $$
CREATE FUNCTION fn_generar_sintomas(p_es_paciente_zero BOOLEAN)
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE v_sintoma VARCHAR(255);
    DECLARE v_intensidad INT;
    DECLARE v_tiempo VARCHAR(50);
    
    IF p_es_paciente_zero = TRUE THEN
        RETURN 'Paciente ingresa en calidad de desconocido. Inconsciente (Escala de Glasgow < 8). Se observan múltiples contusiones y signos de trauma severo. No responde a estímulos verbales ni dolorosos.';
    END IF;
    
    SET v_sintoma = ELT(FLOOR(1 + RAND() * 15),
        'Dolor torácico opresivo irradiado a brazo izquierdo',
        'Disnea de esfuerzo y sensación de ahogo',
        'Cefalea intensa de inicio súbito, pulsátil',
        'Fiebre no cuantificada, escalofríos y diaforesis',
        'Dolor abdominal difuso con rebote y resistencia',
        'Náusea persistente y episodios eméticos de contenido biliar',
        'Debilidad generalizada, astenia y adinamia',
        'Confusión aguda y desorientación',
        'Palpitaciones rápidas e irregulares',
        'Dificultad para movilizar hemicuerpo derecho',
        'Dolor lumbar irradiado a extremidad inferior derecha',
        'Poliuria, polidipsia y visión borrosa',
        'Tos productiva con expectoración verdosa',
        'Sibilancias audibles a distancia y tiraje intercostal',
        'Sangrado transvaginal moderado con coágulos');
        
    SET v_intensidad = FLOOR(1 + RAND() * 10);
    
    SET v_tiempo = ELT(FLOOR(1 + RAND() * 8),
        '3 horas', '12 horas', '24 horas', '2 días', '4 días', '1 semana', '2 semanas', '1 mes');
        
    RETURN CONCAT(v_sintoma, ' | EVA ', v_intensidad, '/10 | Evolución de ', v_tiempo);
END$$
DELIMITER ;
