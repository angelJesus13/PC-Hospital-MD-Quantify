"""
seed_db.py — Poblador de datos de prueba para Quantify Medical API
Crea usuarios, pacientes, notas, diagnósticos y tratamientos de muestra
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, create_tables
from models import (
    MdUsuarios, MdPacientes, MdNotasMedicas, MdDiagnostico,
    MdTratamientos, MdDomicilios, MdPersonasTieneDomicilio,
    MdValoraciones,
)
from auth import hash_password
from datetime import datetime, date, timezone
import logging

logger = logging.getLogger(__name__)


USUARIOS_SEED = [
    {"username": "admin.quantify", "email": "admin@quantify.mx",
     "password": "Admin2026!", "role": "admin"},
    {"username": "dr.garcia", "email": "garcia@quantify.mx",
     "password": "Medico2026!", "role": "medico"},
    {"username": "dra.lopez", "email": "lopez@quantify.mx",
     "password": "Medico2026!", "role": "medico"},
    {"username": "enf.morales", "email": "morales@quantify.mx",
     "password": "Enfermero2026!", "role": "enfermero"},
]

PACIENTES_SEED = [
    {"nombre": "García Hernández Juan", "curp": "GAHJ800312HDFRRN01",
     "fecha_nacimiento": date(1980, 3, 12), "sexo": "M",
     "telefono": "5551234567", "fecha_registro": datetime(2026, 1, 15, 8, 0)},
    {"nombre": "López Martínez María", "curp": "LOMM901201MDFRRR02",
     "fecha_nacimiento": date(1990, 12, 1), "sexo": "F",
     "telefono": "5559876543", "fecha_registro": datetime(2026, 2, 10, 9, 30)},
    {"nombre": "Rodríguez Torres Carlos", "curp": "ROTC750615HDFRRR03",
     "fecha_nacimiento": date(1975, 6, 15), "sexo": "M",
     "telefono": "5554567890", "fecha_registro": datetime(2026, 3, 5, 10, 0)},
    {"nombre": "Sánchez Díaz Ana", "curp": "SADA850920MDFRRR04",
     "fecha_nacimiento": date(1985, 9, 20), "sexo": "F",
     "telefono": "5551357924", "fecha_registro": datetime(2026, 4, 20, 7, 45)},
    {"nombre": "Martínez Flores Pedro", "curp": "MAFP691010HDFRRR05",
     "fecha_nacimiento": date(1969, 10, 10), "sexo": "M",
     "telefono": "5558642097", "fecha_registro": datetime(2026, 5, 1, 11, 0)},
]

DOMICILIOS_SEED = [
    {"calle": "Av. Insurgentes 1245", "colonia": "Santa Fe",
     "municipio": "Álvaro Obregón", "estado": "CDMX", "cp": "01210",
     "latitud": 19.3597, "longitud": -99.2722},
    {"calle": "Calle Reforma 456", "colonia": "Polanco",
     "municipio": "Miguel Hidalgo", "estado": "CDMX", "cp": "11550",
     "latitud": 19.4326, "longitud": -99.1908},
]


def seed_usuarios(db) -> list[MdUsuarios]:
    users = []
    for u in USUARIOS_SEED:
        existing = db.query(MdUsuarios).filter(
            MdUsuarios.username == u["username"]).first()
        if not existing:
            user = MdUsuarios(
                username=u["username"],
                email=u["email"],
                password_hash=hash_password(u["password"]),
                role=u["role"],
            )
            db.add(user)
            users.append(user)
            print(f"  ✅ Usuario creado: {u['username']} [{u['role']}]")
        else:
            users.append(existing)
            print(f"  ⏭️  Usuario ya existe: {u['username']}")
    db.commit()
    return users


def seed_pacientes(db) -> list[MdPacientes]:
    pacientes = []
    for p in PACIENTES_SEED:
        existing = db.query(MdPacientes).filter(
            MdPacientes.curp == p["curp"]).first()
        if not existing:
            paciente = MdPacientes(**p)
            db.add(paciente)
            db.flush()
            pacientes.append(paciente)
            print(f"  ✅ Paciente creado: {p['nombre']}")
        else:
            pacientes.append(existing)
            print(f"  ⏭️  Paciente ya existe: {p['nombre']}")
    db.commit()
    return pacientes


def seed_domicilios(db, pacientes: list[MdPacientes]):
    for i, dom_data in enumerate(DOMICILIOS_SEED):
        dom = MdDomicilios(**dom_data)
        db.add(dom)
        db.flush()
        # Vincular con paciente
        if i < len(pacientes):
            vinculo = MdPersonasTieneDomicilio(
                paciente_id=pacientes[i].id,
                domicilio_id=dom.id,
                tipo_domicilio="principal",
            )
            db.add(vinculo)
            print(f"  ✅ Domicilio vinculado a: {pacientes[i].nombre}")
    db.commit()


def seed_notas_y_diagnosticos(db, pacientes: list[MdPacientes],
                               medico: MdUsuarios):
    # Notas médicas de muestra
    notas_data = [
        {
            "paciente_id": pacientes[0].id,
            "medico_id": medico.id,
            "contenido": "Paciente masculino de 45 años con fiebre de 5 días de evolución, "
                         "tos productiva. SpO2 91% al aire ambiente. RX compatible con neumonía LID.",
            "tipo_nota": "evolucion",
            "fecha": datetime(2026, 5, 21, 10, 0),
        },
        {
            "paciente_id": pacientes[1].id,
            "medico_id": medico.id,
            "contenido": "Paciente femenina de 35 años con HAS conocida. "
                         "TA: 160/100 mmHg. Cefalea intensa. Sin déficit neurológico.",
            "tipo_nota": "urgencias",
            "fecha": datetime(2026, 5, 21, 11, 30),
        },
    ]

    for nd in notas_data:
        nota = MdNotasMedicas(**nd)
        db.add(nota)
        db.flush()
        print(f"  ✅ Nota creada para paciente_id={nd['paciente_id']}")

        # Diagnóstico vinculado
        if nd["tipo_nota"] == "evolucion":
            dx = MdDiagnostico(
                nota_id=nota.id,
                descripcion="Neumonía adquirida en la comunidad",
                codigo_cie="J18.9",
                severidad="grave",
            )
        else:
            dx = MdDiagnostico(
                nota_id=nota.id,
                descripcion="Crisis hipertensiva no urgente",
                codigo_cie="I10",
                severidad="moderado",
            )
        db.add(dx)
        db.flush()

        # Tratamiento
        if nd["tipo_nota"] == "evolucion":
            tx = MdTratamientos(
                diagnostico_id=dx.id,
                medicamento="Amoxicilina-Clavulanato",
                dosis="875/125 mg",
                frecuencia="cada 12 horas",
                duracion="7 días",
                fecha_inicio=datetime(2026, 5, 21, 10, 30),
            )
        else:
            tx = MdTratamientos(
                diagnostico_id=dx.id,
                medicamento="Enalapril",
                dosis="10 mg",
                frecuencia="cada 24 horas",
                duracion="30 días",
                fecha_inicio=datetime(2026, 5, 21, 12, 0),
            )
        db.add(tx)
        print(f"  ✅ Diagnóstico + Tratamiento creados")

    db.commit()


def seed_valoraciones(db, pacientes: list[MdPacientes], medico: MdUsuarios):
    val = MdValoraciones(
        paciente_id=pacientes[2].id,
        escala="Glasgow",
        resultado="8",
        observaciones="TEC severo. GCS=8. Requiere UCI.",
        fecha=datetime(2026, 5, 21, 15, 0),
        registrado_por=medico.id,
    )
    db.add(val)
    db.commit()
    print(f"  ✅ Valoración Glasgow creada para paciente_id={pacientes[2].id}")


def run_seed():
    print("\n" + "═" * 60)
    print("  🌱 Quantify Medical API — Seed DB")
    print("═" * 60)

    db = SessionLocal()
    try:
        create_tables()
        print("\n📋 Creando usuarios...")
        users = seed_usuarios(db)

        print("\n👥 Creando pacientes...")
        pacientes = seed_pacientes(db)

        print("\n🏠 Creando domicilios...")
        seed_domicilios(db, pacientes)

        medico = next(u for u in users if u.role == "medico")
        print(f"\n📝 Creando notas médicas (médico: {medico.username})...")
        seed_notas_y_diagnosticos(db, pacientes, medico)

        print("\n📊 Creando valoraciones...")
        seed_valoraciones(db, pacientes, medico)

        print("\n" + "═" * 60)
        print("  ✅ Seed completado exitosamente!")
        print("═" * 60 + "\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error durante el seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
