# Generadores de datos sintéticos para pruebas

Este repositorio contiene scripts y artefactos generados para pruebas funcionales y de performance de un sistema bancario. Aquí se documentan los pasos que ejecuté, los artefactos creados y las instrucciones para reproducir las cargas en PostgreSQL.

Contenido principal
- `scripts/generate_customers.py` — genera 1000 clientes sintéticos y escribe `scripts/clientes_1000.json`.
- `scripts/generate_transactions_sql.py` — genera 10,000 INSERTs y escribe `scripts/transacciones_10000.sql`.
- `scripts/clientes_1000.json` / `scripts/clientes_1000.csv` — dataset de clientes (JSON y CSV).
- `scripts/transacciones_10000.sql` / `scripts/transacciones_10000.csv` — sentencias INSERT (SQL) y versión en CSV.
- `scripts/transacciones_10000_inserts.csv` — cada fila contiene una sentencia INSERT (texto).
- `scripts/splits/transacciones_inserts_part_01.csv` ... `_part_10.csv` — división del CSV de INSERTs para cargas paralelas.
- `scripts/load_into_postgres.psql` — script psql que crea tablas y usa `\copy` para cargar los CSVs.
- `reports/report_escenarios.html` — reporte HTML con estadísticas y muestras.
- `reports/escenarios_automatizados.csv` — resumen clave/valor de los escenarios ejecutados.
- `reports/images/*` — gráficos generados (PNG) para distribuciones por tipo/estado/canal.

Fechas y entorno
- Fecha de ejecución/entrada: 2025-12-11
- Entorno Python usado: `.venv` del repo (Python 3.11). Ejecución de ejemplo en PowerShell con la ruta del intérprete en `C:/Users/2490109/Taller3CarlosQA/Taller3CarlosQA/.venv/Scripts/python.exe`.

Pasos ejecutados (ordenados y reproducibles)

1) Generar clientes (1000 registros)

```powershell
cd 'c:\Users\2490109\Taller3CarlosQA\Taller3CarlosQA\scripts'
C:/Users/2490109/Taller3CarlosQA/Taller3CarlosQA/.venv/Scripts/python.exe .\generate_customers.py
```

Salida: `scripts/clientes_1000.json` y (posterior) `scripts/clientes_1000.csv`.

2) Generar transacciones (10,000 INSERTs)

```powershell
cd 'c:\Users\2490109\Taller3CarlosQA\Taller3CarlosQA\scripts'
C:/Users/2490109/Taller3CarlosQA/Taller3CarlosQA/.venv/Scripts/python.exe .\generate_transactions_sql.py
```

Salida: `scripts/transacciones_10000.sql`.

Reglas de negocio aplicadas por el generador de transacciones
- 500 cuentas (`ACC-00001`..`ACC-00500`).
- Fechas distribuidas uniformemente en los últimos 2 años y orden cronológico garantizado en el SQL final.
- Distribuciones por tipo/estado/canal conforme al requerimiento: TRANSFERENCIA 40% / DEPOSITO 25% / RETIRO 20% / PAGO_SERVICIO 15%; EXITOSA 85% / PENDIENTE 10% / RECHAZADA 5%; APP_MOVIL 50% / WEB 30% / CAJERO 15% / SUCURSAL 5%.
- Montos generados dentro de los rangos solicitados por tipo.
- Transferencias con `id_cuenta_origen != id_cuenta_destino`.
- Depósitos y Retiros con `id_cuenta_destino = NULL`.
- Límite de 50 transacciones por cuenta por día (controlado heurísticamente durante la generación).

3) Convertir SQL a CSV / generar CSVs auxiliares

- Convertí `transacciones_10000.sql` a `scripts/transacciones_10000.csv` (columnas: `id_transaccion,fecha_hora,id_cuenta_origen,id_cuenta_destino,tipo_transaccion,monto,estado,canal,descripcion`).
- Generé `scripts/transacciones_10000_inserts.csv` (texto de cada INSERT en una fila) y lo dividí en 10 archivos en `scripts/splits/` para cargas paralelas: `transacciones_inserts_part_01.csv` ... `part_10.csv`.

4) Generar reportes y gráficos

- Generé `reports/report_escenarios.html` con estadísticas (conteos por tipo/estado/canal, distribución por ciudad, verificación del límite 50 tx/día, muestras).  
- Generé gráficos PNG en `reports/images/`:
	- `tipo_bar.png`, `tipo_pie.png`
	- `estado_bar.png`, `estado_pie.png`
	- `canal_bar.png`, `canal_pie.png`

5) Script para carga a PostgreSQL (cliente):

- `scripts/load_into_postgres.psql` contiene SQL para crear tablas `clientes` y `transacciones` y usa `\copy` para importar `scripts/clientes_1000.csv` y `scripts/transacciones_10000.csv`.

Ejemplo de ejecución (cliente):

```powershell
# desde máquina con psql instalado y acceso al servidor
psql -h <HOST> -U <USER> -d <DB> -f scripts/load_into_postgres.psql
```

Si prefieres realizar cargas paralelas con los archivos split (por ejemplo, `transacciones_inserts_part_01.csv`), existen dos opciones:

- Opción A — ejecutar los `\copy` de `transacciones_10000.csv` (una sola carga). Más simple y rápido para datasets medianos.
- Opción B — para cargas masivas con múltiples workers, puedes usar las partes con `psql` y `\copy` en paralelo en varios procesos. Ejemplo PowerShell:

```powershell
# Ejecuta 10 cargas en paralelo (ajusta las rutas y credenciales)
for ($i=1; $i -le 10; $i++) {
	$part = "scripts/splits/transacciones_inserts_part_{0:00}.csv" -f $i
	Start-Job -ScriptBlock { param($p) psql -h <HOST> -U <USER> -d <DB> -c "\copy transacciones FROM '" + $p + "' WITH (FORMAT csv, HEADER true)" } -ArgumentList $part
}
# Luego esperar a que terminen: Get-Job | Wait-Job
```

6) Artefactos añadidos al repositorio

- `scripts/clientes_1000.json`, `scripts/clientes_1000.csv`
- `scripts/transacciones_10000.sql`, `scripts/transacciones_10000.csv`
- `scripts/transacciones_10000_inserts.csv` y `scripts/splits/*`
- `scripts/generate_customers.py`, `scripts/generate_transactions_sql.py`
- `scripts/load_into_postgres.psql`
- `reports/report_escenarios.html`, `reports/escenarios_automatizados.csv`, `reports/images/*`

Notas finales
- Los scripts son reproducibles: la semilla del generador está fijada para resultados determinísticos. Cambia o elimina `random.seed(...)` para generar variaciones.
- Si necesitas que retire los archivos generados del repo y deje sólo los scripts, dímelo y los muevo a una carpeta `artifacts/` o los elimino del control de versiones.

Contacto
- Si quieres que automatice la carga en un entorno de pruebas (preparar Playbook/PowerShell que ejecute las cargas y verifique conteos), puedo prepararlo.

