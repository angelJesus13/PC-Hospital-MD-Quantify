-- ============================================================
-- init_db.sql — Script de inicialización de base de datos MySQL
-- PC-Hospital-MD-Quantify | Quantify Medical Hybrid API
-- Motor: MySQL 8.0+  | Charset: utf8mb4
-- ============================================================

SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS `quantify_medical_db`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `quantify_medical_db`;

-- ─────────────────────────────────────────────────────────────
-- 1. md_usuarios
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_usuarios` (
  `id`            INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `username`      VARCHAR(80)     NOT NULL,
  `email`         VARCHAR(120)    NOT NULL,
  `password_hash` VARCHAR(200)    NOT NULL COMMENT 'bcrypt hash, costo=12',
  `role`          ENUM('admin','medico','enfermero') NOT NULL DEFAULT 'medico',
  `activo`        BOOLEAN         NOT NULL DEFAULT TRUE,
  `created_at`    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`    DATETIME        NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_usuarios_username` (`username`),
  UNIQUE KEY `idx_usuarios_email` (`email`),
  KEY `idx_usuarios_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────────────
-- 2. md_pacientes
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_pacientes` (
  `id`               INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `nombre`           VARCHAR(100)    NOT NULL,
  `curp`             CHAR(18)        NOT NULL,
  `fecha_nacimiento` DATE            NULL,
  `sexo`             ENUM('M','F','NB') NULL,
  `telefono`         VARCHAR(15)     NULL,
  `fecha_registro`   DATETIME        NOT NULL,
  `created_at`       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_pacientes_curp` (`curp`),
  KEY `idx_pacientes_nombre` (`nombre`),
  KEY `idx_pacientes_fecha_registro` (`fecha_registro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────────────
-- 3. md_notas_medicas
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_notas_medicas` (
  `id`          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `paciente_id` INT UNSIGNED    NOT NULL,
  `medico_id`   INT UNSIGNED    NOT NULL,
  `contenido`   TEXT            NOT NULL,
  `tipo_nota`   ENUM('ingreso','evolucion','egreso','interconsulta','urgencias') NOT NULL,
  `fecha`       DATETIME        NOT NULL,
  `created_at`  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_notas_paciente_fecha` (`paciente_id`, `fecha`),
  KEY `idx_notas_medico` (`medico_id`),
  KEY `idx_notas_tipo` (`tipo_nota`),
  CONSTRAINT `fk_notas_paciente`
    FOREIGN KEY (`paciente_id`) REFERENCES `md_pacientes` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_notas_medico`
    FOREIGN KEY (`medico_id`) REFERENCES `md_usuarios` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────────────
-- 4. md_signos_vitales
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_signos_vitales` (
  `id`                    INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `paciente_id`           INT UNSIGNED    NOT NULL,
  `tension_arterial`      VARCHAR(20)     NULL COMMENT 'formato: sist/diast',
  `frecuencia_cardiaca`   INT UNSIGNED    NULL COMMENT 'lpm (0-300)',
  `temperatura`           DECIMAL(5,2)    NULL COMMENT 'Celsius (30-45)',
  `frecuencia_respiratoria` INT UNSIGNED  NULL COMMENT 'rpm (0-60)',
  `saturacion_o2`         INT UNSIGNED    NULL COMMENT '% (0-100)',
  `escala_consciencia`    VARCHAR(30)     NULL,
  `score_mews`            INT UNSIGNED    NOT NULL DEFAULT 0,
  `fecha`                 DATETIME        NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_sv_paciente_fecha` (`paciente_id`, `fecha` DESC),
  KEY `idx_sv_score_mews` (`score_mews`),
  CONSTRAINT `fk_sv_paciente`
    FOREIGN KEY (`paciente_id`) REFERENCES `md_pacientes` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `chk_sv_fc`
    CHECK (`frecuencia_cardiaca` BETWEEN 0 AND 300),
  CONSTRAINT `chk_sv_temp`
    CHECK (`temperatura` BETWEEN 30.0 AND 45.0),
  CONSTRAINT `chk_sv_spo2`
    CHECK (`saturacion_o2` BETWEEN 0 AND 100),
  CONSTRAINT `chk_sv_fr`
    CHECK (`frecuencia_respiratoria` BETWEEN 0 AND 60)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────────────
-- 5. md_diagnostico
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_diagnostico` (
  `id`          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `nota_id`     INT UNSIGNED    NOT NULL,
  `descripcion` TEXT            NOT NULL,
  `codigo_cie`  CHAR(7)         NULL COMMENT 'CIE-10: A99.9',
  `severidad`   ENUM('leve','moderado','grave','critico') NOT NULL DEFAULT 'leve',
  `activo`      BOOLEAN         NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`id`),
  KEY `idx_dx_nota` (`nota_id`),
  KEY `idx_dx_codigo_cie` (`codigo_cie`),
  KEY `idx_dx_severidad` (`severidad`),
  CONSTRAINT `fk_dx_nota`
    FOREIGN KEY (`nota_id`) REFERENCES `md_notas_medicas` (`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────────────
-- 6. md_tratamientos
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_tratamientos` (
  `id`              INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `diagnostico_id`  INT UNSIGNED    NOT NULL,
  `medicamento`     VARCHAR(200)    NOT NULL,
  `dosis`           VARCHAR(50)     NOT NULL,
  `frecuencia`      VARCHAR(50)     NOT NULL,
  `duracion`        VARCHAR(30)     NOT NULL,
  `activo`          BOOLEAN         NOT NULL DEFAULT TRUE,
  `fecha_inicio`    DATETIME        NULL,
  `fecha_fin`       DATETIME        NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tx_diagnostico` (`diagnostico_id`),
  KEY `idx_tx_activo` (`activo`),
  KEY `idx_tx_medicamento` (`medicamento`),
  CONSTRAINT `fk_tx_dx`
    FOREIGN KEY (`diagnostico_id`) REFERENCES `md_diagnostico` (`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────────────
-- 7. md_nacimientos
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_nacimientos` (
  `id`               INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `paciente_id`      INT UNSIGNED    NOT NULL,
  `fecha_nacimiento` DATE            NOT NULL,
  `lugar`            VARCHAR(200)    NOT NULL,
  `nombre_madre`     VARCHAR(100)    NULL,
  `nombre_padre`     VARCHAR(100)    NULL,
  `peso_al_nacer`    DECIMAL(5,2)    NULL COMMENT 'kg',
  `talla_al_nacer`   DECIMAL(5,2)    NULL COMMENT 'cm',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_nac_paciente` (`paciente_id`),
  CONSTRAINT `fk_nac_paciente`
    FOREIGN KEY (`paciente_id`) REFERENCES `md_pacientes` (`id`)
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────────────
-- 8. md_defunciones
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_defunciones` (
  `id`               INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `paciente_id`      INT UNSIGNED    NOT NULL,
  `fecha_defuncion`  DATETIME        NOT NULL,
  `causa`            TEXT            NOT NULL,
  `causa_basica`     TEXT            NULL,
  `certificador`     VARCHAR(50)     NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_def_paciente` (`paciente_id`),
  KEY `idx_def_fecha` (`fecha_defuncion`),
  CONSTRAINT `fk_def_paciente`
    FOREIGN KEY (`paciente_id`) REFERENCES `md_pacientes` (`id`)
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────────────
-- 9. md_documentos_oficiales
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_documentos_oficiales` (
  `id`                INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `paciente_id`       INT UNSIGNED    NOT NULL,
  `tipo_documento`    ENUM('ine','curp','nss','pasaporte','acta_nacimiento') NOT NULL,
  `numero_documento`  VARCHAR(60)     NOT NULL,
  `fecha_emision`     DATE            NULL,
  `fecha_vencimiento` DATE            NULL,
  `vigente`           BOOLEAN         NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`id`),
  KEY `idx_docs_paciente` (`paciente_id`),
  KEY `idx_docs_tipo` (`tipo_documento`),
  UNIQUE KEY `idx_docs_numero` (`tipo_documento`, `numero_documento`),
  CONSTRAINT `fk_docs_paciente`
    FOREIGN KEY (`paciente_id`) REFERENCES `md_pacientes` (`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────────────
-- 10. md_domicilios
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_domicilios` (
  `id`         INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `calle`      VARCHAR(200)    NOT NULL,
  `colonia`    VARCHAR(100)    NOT NULL,
  `municipio`  VARCHAR(100)    NOT NULL,
  `estado`     VARCHAR(60)     NOT NULL,
  `cp`         CHAR(5)         NOT NULL,
  `latitud`    DECIMAL(10,7)   NULL,
  `longitud`   DECIMAL(10,7)   NULL,
  PRIMARY KEY (`id`),
  KEY `idx_dom_municipio` (`municipio`),
  KEY `idx_dom_estado` (`estado`),
  KEY `idx_dom_cp` (`cp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────────────
-- 11. md_personas_tiene_domicilio
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_personas_tiene_domicilio` (
  `id`             INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `paciente_id`    INT UNSIGNED    NOT NULL,
  `domicilio_id`   INT UNSIGNED    NOT NULL,
  `tipo_domicilio` ENUM('principal','temporal','referencia') NOT NULL DEFAULT 'principal',
  `activo`         BOOLEAN         NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_ptd_unique` (`paciente_id`, `domicilio_id`, `tipo_domicilio`),
  KEY `idx_ptd_paciente` (`paciente_id`),
  KEY `idx_ptd_domicilio` (`domicilio_id`),
  CONSTRAINT `fk_ptd_paciente`
    FOREIGN KEY (`paciente_id`) REFERENCES `md_pacientes` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_ptd_domicilio`
    FOREIGN KEY (`domicilio_id`) REFERENCES `md_domicilios` (`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────────────────────
-- 12. md_valoraciones
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS `md_valoraciones` (
  `id`              INT UNSIGNED    NOT NULL AUTO_INCREMENT,
  `paciente_id`     INT UNSIGNED    NOT NULL,
  `escala`          VARCHAR(50)     NOT NULL,
  `resultado`       VARCHAR(10)     NULL,
  `observaciones`   TEXT            NULL,
  `fecha`           DATETIME        NOT NULL,
  `registrado_por`  INT UNSIGNED    NULL,
  PRIMARY KEY (`id`),
  KEY `idx_val_paciente_fecha` (`paciente_id`, `fecha` DESC),
  KEY `idx_val_escala` (`escala`),
  CONSTRAINT `fk_val_paciente`
    FOREIGN KEY (`paciente_id`) REFERENCES `md_pacientes` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_val_usuario`
    FOREIGN KEY (`registrado_por`) REFERENCES `md_usuarios` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `chk_val_escala`
    CHECK (`escala` IN ('Glasgow','MEWS','APGAR','Braden','Norton','SOFA'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- ─────────────────────────────────────────────────────────────
-- Datos iniciales: usuario admin por defecto
-- Contraseña: Admin2026! (cambiar inmediatamente en producción)
-- ─────────────────────────────────────────────────────────────
INSERT IGNORE INTO `md_usuarios` (`username`, `email`, `password_hash`, `role`) VALUES
('admin.quantify', 'admin@quantify.mx',
 '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMqJqhcanFp8.w1c9gHb5NKIY2', 'admin');
-- Hash corresponde a: Admin2026!

SELECT 'Base de datos inicializada correctamente ✅' AS status;
