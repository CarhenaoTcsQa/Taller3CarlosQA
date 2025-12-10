# Script para generar 1000 clientes sintéticos en formato JSON
# Cumple con las reglas solicitadas por el usuario (colombia, distribución, validaciones)
import json
import random
from datetime import datetime

OUT_FILE = "clientes_1000.json"
TOTAL = 1000
DATE_TAG = "20251210"  # Fecha usada en los IDs: CLT-YYYYMMDD-NNNN

first_names = [
    "Juan", "Carlos", "Andrés", "Diego", "Santiago", "David", "Luis", "José", "Javier", "Alejandro",
    "María", "Catalina", "Laura", "Andrea", "Paula", "Angela", "Luisa", "Sofía", "Valentina", "Daniela"
]
middle_names = ["Fernando","Miguel","Esteban","Gustavo","Ricardo","Patricia","Rosario","Marisol","Natalia","Claudia"]
last_names = [
    "González","Rodríguez","Martínez","Gómez","López","Pérez","Sánchez","Ramírez","Torres","Ruiz",
    "Castillo","Vargas","Rojas","Mendoza","Cárdenas","Herrera","Díaz","Vega","Ospina","Cruz"
]

company_domains = ["banco.com.co","financiera.com.co","grupoempresa.com","corp.com.co","servicios.com.co"]

# Cities distribution counts
cities = (['Bogotá'] * 400) + (['Medellín'] * 200) + (['Cali'] * 150) + (['Barranquilla'] * 80) + (['Cartagena'] * 55) + (['Bucaramanga'] * 15)
# total 400+200+150+80+55+15 = 900 -> adjust to 1000 by adding more 'Otras'
while len(cities) < TOTAL:
    cities.append(random.choice(["Pereira","Manizales","Ibagué","Montería","Santa Marta","Sincelejo","Neiva"]))
random.shuffle(cities)

# Profile groups by distribution (Excellent 20%, Good 40%, Regular 30%, Bad 10%)
profiles = (['Excelente'] * 200) + (['Bueno'] * 400) + (['Regular'] * 300) + (['Malo'] * 100)
random.shuffle(profiles)

customers = []
cedula_base = 1000000000
phone_base = 3000000000

for i in range(TOTAL):
    idx = i + 1
    # ID
    id_str = f"CLT-{DATE_TAG}-{idx:04d}"

    # Cedula (10 dígitos)
    cedula = str(cedula_base + i)

    # Name generation
    fn = first_names[i % len(first_names)]
    mn = middle_names[i % len(middle_names)] if (i % 5 == 0) else ""
    ln1 = last_names[i % len(last_names)]
    ln2 = last_names[(i + 3) % len(last_names)]
    if mn:
        nombre_completo = f"{fn} {mn} {ln1} {ln2}"
    else:
        nombre_completo = f"{fn} {ln1} {ln2}"

    # Email unique (corporate format)
    domain = company_domains[i % len(company_domains)]
    local_part = f"{fn.lower()}.{ln1.lower()}{idx%1000:03d}"
    email = f"{local_part}@{domain}"

    # Telefono
    phone_num = phone_base + i
    # Format as +57 3XX XXX XXXX
    s = str(phone_num)
    telefono = f"+57 {s[0:3]} {s[3:6]} {s[6:10]}"

    # Fecha de nacimiento: years 1960-2000
    year = 1960 + (i % 41)  # 1960..2000
    month = (i % 12) + 1
    day = (i % 28) + 1
    fecha_nac = f"{year:04d}-{month:02d}-{day:02d}"

    # Edad aproximada
    age = 2025 - year

    # Tipo empleo: 70% Empleado, 20% Independiente, 10% Pensionado
    r = random.random()
    if r < 0.7:
        tipo_empleo = "Empleado"
    elif r < 0.9:
        tipo_empleo = "Independiente"
    else:
        tipo_empleo = "Pensionado"

    # Antiguedad laboral: 0-30 años consistent con edad
    max_ant = max(0, min(30, age - 18))
    antiguedad = random.randint(0, max_ant) if max_ant > 0 else 0

    # Ciudad
    ciudad = cities[i]

    # Ingreso mensual (1.500.000 - 20.000.000 COP)
    ingreso = 1500000 + ((i * 123457) % (20000000 - 1500000 + 1))

    # Saldo cuenta de ahorros 0 - 50.000.000
    saldo_ahorros = ((i * 76543) % 50000001)

    # Perfil (historial crediticio) from shuffled profiles
    historial = profiles[i]

    # Score consistent with historial
    if historial == 'Excelente':
        score = random.randint(750, 850)
        debt_pct = random.randint(1, 19)  # <20%
    elif historial == 'Bueno':
        score = random.randint(650, 749)
        debt_pct = random.randint(20, 39)
    elif historial == 'Regular':
        score = random.randint(550, 649)
        debt_pct = random.randint(40, 59)
    else:  # Malo
        score = random.randint(300, 549)
        debt_pct = random.randint(60, 80)

    # deudaActual: porcentaje del ingreso mensual, no excede 80%
    deuda = int(round(ingreso * debt_pct / 100.0))

    customer = {
        "id": id_str,
        "cedulaCiudadania": cedula,
        "nombreCompleto": nombre_completo,
        "email": email,
        "telefono": telefono,
        "fechaNacimiento": fecha_nac,
        "ciudadResidencia": ciudad,
        "ingresoMensual": ingreso,
        "tipoEmpleo": tipo_empleo,
        "antiguedadLaboral": antiguedad,
        "historialCrediticio": historial,
        "deudaActual": deuda,
        "saldoCuentaAhorros": saldo_ahorros,
        "scoreCrediticio": score
    }

    customers.append(customer)

# Escribir JSON de salida
with open(OUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(customers, f, ensure_ascii=False, indent=2)

print(f"Generados {len(customers)} clientes en {OUT_FILE}")
