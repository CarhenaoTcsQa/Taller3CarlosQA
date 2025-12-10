# Generadores de datos sintéticos para pruebas

Este repositorio contiene scripts para generar datos sintéticos usados en pruebas de un sistema bancario (pruebas funcionales y de performance).

Contenido relevante:
- `scripts/generate_customers.py`: genera 1000 clientes sintéticos en JSON (`clientes_1000.json`).
- `scripts/generate_transactions_sql.py`: genera 10,000 INSERTs SQL para la tabla `transacciones` en `transacciones_10000.sql`.
- `scripts/clientes_1000.json`: dataset de 1000 clientes generado.
- `scripts/transacciones_10000.sql`: SQL con 10,000 INSERTs generado.

Cómo se ejecutó (pasos reproducibles):

1. Generador de clientes (1000 registros)

```powershell
cd 'c:\Users\2490109\Taller3CarlosQA\Taller3CarlosQA\scripts'
# Ejecutar con el intérprete Python del entorno (si usa el venv del repo):
C:/Users/2490109/Taller3CarlosQA/Taller3CarlosQA/.venv/Scripts/python.exe .\generate_customers.py
```

Salida: `clientes_1000.json` (valores: id formato `CLT-YYYYMMDD-NNNN`, cédulas únicas, emails únicos, score consistente con historial, distribución por ciudad y perfil).

2. Generador de transacciones (10,000 INSERTs)

```powershell
cd 'c:\Users\2490109\Taller3CarlosQA\Taller3CarlosQA\scripts'
C:/Users/2490109/Taller3CarlosQA/Taller3CarlosQA/.venv/Scripts/python.exe .\generate_transactions_sql.py
```

Salida: `transacciones_10000.sql` con `BEGIN;` ... `COMMIT;` y 10,000 sentencias `INSERT INTO transacciones (...) VALUES (...);`.

Reglas aplicadas por el generador de transacciones:
- 500 cuentas (`ACC-00001`..`ACC-00500`).
- Fechas uniformemente distribuidas en los últimos 2 años y ordenadas cronológicamente.
- Tipos de transacción con distribución: TRANSFERENCIA 40%, DEPOSITO 25%, RETIRO 20%, PAGO_SERVICIO 15%.
- Montos por tipo dentro de los rangos pedidos.
- Estado con distribución: EXITOSA 85%, PENDIENTE 10%, RECHAZADA 5% (rechazos sólo para TRANSFERENCIA y RETIRO).
- Canal con distribución: APP_MOVIL 50%, WEB 30%, CAJERO 15%, SUCURSAL 5%.
- Transferencias con `id_cuenta_origen != id_cuenta_destino`.
- Depósitos y Retiros con `id_cuenta_destino = NULL`.
- Límite aproximado: máximo 50 transacciones por cuenta por día (controlado en la lógica del generador).

Verificaciones rápidas sugeridas (ejemplos):

```sql
-- contar registros
SELECT count(*) FROM transacciones; -- debe ser 10000

-- contar por tipo
SELECT tipo_transaccion, count(*) FROM transacciones GROUP BY tipo_transaccion;

-- asegurar transferencias tienen destino
SELECT count(*) FROM transacciones WHERE tipo_transaccion='TRANSFERENCIA' AND id_cuenta_destino IS NULL;

-- rechazos sólo para TRANSFERENCIA y RETIRO
SELECT distinct tipo_transaccion FROM transacciones WHERE estado='RECHAZADA';
```

Notas:
- Los scripts usan valores pseudoaleatorios (semilla fija) para reproducibilidad. Cambiar `random.seed(...)` en los scripts para variar los datos.
- `transacciones_10000.sql` incluye `BEGIN;` y `COMMIT;` para facilitar su carga en PostgreSQL.

Si deseas, puedo:
- Hacer `git commit` y `git push` (ya lo hice si autorizas).  
- Proveer una versión CSV del dataset de clientes o particionar el SQL en ficheros más pequeños.

Contacto: especialista en generación de datos sintéticos para banca.
