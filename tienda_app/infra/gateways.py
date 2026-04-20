import datetime
from pathlib import Path
from ..domain.interfaces import ProcesadorPago


class BancoNacionalProcesador(ProcesadorPago):

    def pagar(self, monto: float) -> bool:

        # Crear ruta del archivo de log en el directorio del proyecto
        base_dir = Path(__file__).parent.parent.parent
        archivo_log = base_dir / "pagos_locales_DAVID_RODRIGUEZ.log"

        with open(archivo_log, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] Transaccion exitosa por: ${monto}\n")

        return True