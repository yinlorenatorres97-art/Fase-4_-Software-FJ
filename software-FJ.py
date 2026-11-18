# ============================================================
# SISTEMA INTEGRAL DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS
# ============================================================

# importación librerias#

from abc import ABC, abstractmethod
from datetime import datetime
import logging

# ============================================================
# 1. CONFIGURACION DEL SISTEMA DE REGISTROS
# ============================================================

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

# ============================================================
# 2. EXCEPCIONES PERSONALIZADAS
# ============================================================


class ErrorSistema(Exception):
    pass


class ErrorValidacion(ErrorSistema):
    pass


class ErrorServicio(ErrorSistema):
    pass


class ErrorReserva(ErrorSistema):
    pass


class ErrorCliente(ErrorSistema):
    pass


# ============================================================
# 3. CLASE ABSTRACTA GENERAL: ENTIDAD
# ============================================================


class Entidad(ABC):

    def __init__(self, identificacion, nombre):
        self._identificacion = identificacion
        self._nombre = nombre

    @property
    def identificacion(self):
        return self._identificacion

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def mostrar_informacion(self):
        pass


# ============================================================
# 4. CLASE CLIENTE (Hija)
# ============================================================


class Cliente(Entidad):

    def __init__(self, nombre, documento, correo, telefono):

        if not isinstance(nombre, str) or not nombre.strip():
            raise ErrorValidacion("El nombre es obligatorio.")

        if not isinstance(documento, str) or not documento.isdigit():
            raise ErrorValidacion("El documento debe contener solo numeros.")

        if not isinstance(correo, str) or "@" not in correo or "." not in correo:
            raise ErrorValidacion("El correo electronico no es valido.")

        if not isinstance(telefono, str) or not telefono.isdigit():
            raise ErrorValidacion("El telefono debe contener solo numeros.")

        super().__init__(documento, nombre.strip())

        self.__correo = correo
        self.__telefono = telefono

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_informacion(self):
        print("\n--- INFORMACION DEL CLIENTE ---")
        print("Nombre:", self.nombre)
        print("Documento:", self.identificacion)
        print("Correo:", self.__correo)
        print("Telefono:", self.__telefono)


# 5. CLASE ABSTRACTA SERVICIO
# ============================================================


class Servicio(Entidad):

    def __init__(self, identificacion, nombre, tarifa):

        if (
            not isinstance(tarifa, (int, float))
            or isinstance(tarifa, bool)
            or tarifa <= 0
        ):
            raise ErrorServicio("La tarifa debe ser un numero mayor que cero.")

        super().__init__(identificacion, nombre)

        self._tarifa = float(tarifa)
        self._disponible = True

    @property
    def tarifa(self):
        return self._tarifa

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado):
        if not isinstance(estado, bool):
            raise ErrorServicio("El estado debe ser verdadero o falso.")
        self._disponible = estado

    @abstractmethod
    def calcular_costo_base(self, duracion):
        pass

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    # Simulacion de sobrecarga mediante parametros opcionales
    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        self.validar_parametros(duracion)

        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or not 0 <= impuesto <= 100
        ):
            raise ErrorValidacion("El impuesto debe estar entre 0 y 100.")

        if (
            not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not 0 <= descuento <= 100
        ):
            raise ErrorValidacion("El descuento debe estar entre 0 y 100.")

        costo_base = self.calcular_costo_base(duracion)
        costo_descuento = costo_base * (1 - descuento / 100)
        costo_final = costo_descuento * (1 + impuesto / 100)

        return round(costo_final, 2)


# ============================================================
# 6. SERVICIO ESPECIALIZADO: RESERVA DE SALAS
# ============================================================


class ServicioSala(Servicio):

    def calcular_costo_base(self, duracion):
        self.validar_parametros(duracion)
        return self.tarifa * duracion

    def describir(self):
        return "Alquiler de salas por horas."

    def validar_parametros(self, duracion):

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):
            raise ErrorServicio("La duracion de la sala debe ser mayor que cero.")

        if not self.disponible:
            raise ErrorServicio("La sala no esta disponible.")

    def mostrar_informacion(self):
        print(f"{self.identificacion} - {self.nombre} - Sala - ${self.tarifa}/hora")


# ============================================================
# 7. SERVICIO ESPECIALIZADO: ALQUILER DE EQUIPOS
# ============================================================


class ServicioEquipo(Servicio):

    def calcular_costo_base(self, duracion):
        self.validar_parametros(duracion)
        return self.tarifa * duracion

    def describir(self):
        return "Alquiler de equipos tecnologicos por dias."

    def validar_parametros(self, duracion):

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):
            raise ErrorServicio("La cantidad de dias debe ser mayor que cero.")

        if not self.disponible:
            raise ErrorServicio("El equipo no esta disponible.")

    def mostrar_informacion(self):
        print(f"{self.identificacion} - {self.nombre} - Equipo - ${self.tarifa}/dia")


# ============================================================
# 8. SERVICIO ESPECIALIZADO: ASESORIAS
# ============================================================


class ServicioAsesoria(Servicio):

    def calcular_costo_base(self, duracion):
        self.validar_parametros(duracion)
        return self.tarifa * duracion

    def describir(self):
        return "Asesorias especializadas por horas."

    def validar_parametros(self, duracion):

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):
            raise ErrorServicio("La duracion de la asesoria debe ser mayor que cero.")

        if not self.disponible:
            raise ErrorServicio("La asesoria no esta disponible.")

    def mostrar_informacion(self):
        print(f"{self.identificacion} - {self.nombre} - Asesoria - ${self.tarifa}/hora")


# ======================================
# 9. CLASE RESERVA
# ============================================================

class Reserva(Entidad):

    def __init__(self, identificacion, cliente, servicio, duracion):

        # Validar que el cliente sea un objeto de tipo Cliente
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Debe seleccionar un cliente valido.")

        # Validar que el servicio sea un objeto de tipo Servicio
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Debe seleccionar un servicio valido.")

        # Validar los parámetros de duración del servicio
        servicio.validar_parametros(duracion)

        # Inicializar los atributos heredados de Entidad
        super().__init__(identificacion, f"Reserva {identificacion}")

        # Atributos privados de la reserva
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"
        self.__fecha = datetime.now()
        self.__costo = None

    # --------------------------------------------------------
    # PROPIEDADES
    # --------------------------------------------------------

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    # --------------------------------------------------------
    # MÉTODO PARA CONFIRMAR LA RESERVA
    # --------------------------------------------------------

    def confirmar(self):

        if self.__estado != "Pendiente":
            raise ErrorReserva(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.__estado = "Confirmada"

        logging.info(
            "Reserva %s confirmada.",
            self.identificacion
        )

        print("Reserva confirmada correctamente.")

    # --------------------------------------------------------
    # MÉTODO PARA CANCELAR LA RESERVA
    # --------------------------------------------------------

    def cancelar(self):

        if self.__estado not in ("Pendiente", "Confirmada"):
            raise ErrorReserva(
                "No se puede cancelar una reserva procesada o cancelada."
            )

        self.__estado = "Cancelada"

        logging.info(
            "Reserva %s cancelada.",
            self.identificacion
        )

        print("Reserva cancelada correctamente.")

    # --------------------------------------------------------
    # MÉTODO PARA PROCESAR LA RESERVA
    # --------------------------------------------------------

    def procesar(self, impuesto=0, descuento=0):

        if self.__estado != "Confirmada":
            raise ErrorReserva(
                "La reserva debe estar confirmada para procesarse."
            )

        try:
            self.__costo = self.__servicio.calcular_costo(
                self.__duracion,
                impuesto,
                descuento
            )

            self.__estado = "Procesada"

        except ErrorSistema as error:

            logging.exception(
                "Error procesando la reserva."
            )

            raise ErrorReserva(
                "No fue posible procesar el costo de la reserva."
            ) from error

        logging.info(
            "Reserva %s procesada. Costo: $%s",
            self.identificacion,
            self.__costo
        )

        print("Reserva procesada correctamente.")
        print("Costo total: $", self.__costo)

        return self.__costo

    # --------------------------------------------------------
    # MÉTODO PARA MOSTRAR LA INFORMACIÓN
    # --------------------------------------------------------

    def mostrar_informacion(self):

        print("\n--- INFORMACION DE LA RESERVA ---")

        print("Codigo:", self.identificacion)
        print("Cliente:", self.cliente.nombre)
        print("Servicio:", self.servicio.nombre)
        print("Duracion:", self.duracion)
        print("Estado:", self.estado)

        print(
            "Fecha:",
            self.__fecha.strftime("%d/%m/%Y %H:%M")
        )

        if self.__costo is not None:
            print("Costo:", self.__costo)


# ============================================================
# 10. CLASE PRINCIPAL: SISTEMA SOFTWARE FJ
# ============================================================

class SistemaSoftwareFJ:

    def __init__(self, cargar_servicios=True):

        self.clientes = []
        self.servicios = []
        self.reservas = []

        if cargar_servicios:
            self.cargar_servicios_iniciales()

    def cargar_servicios_iniciales(self):

        servicios = [
            ServicioSala("S01", "Sala de reuniones", 5000),
            ServicioEquipo("E01", "Computador portatil", 8000),
            ServicioAsesoria("A01", "Asesoria informatica", 10000)
        ]

        for servicio in servicios:
            self.agregar_servicio(servicio)

    # REGISTRAR CLIENTE

    def registrar_cliente(self, nombre, documento, correo, telefono):

        if any(c.identificacion == documento for c in self.clientes):
            raise ErrorCliente("El documento ya se encuentra registrado.")

        cliente = Cliente(nombre, documento, correo, telefono)
        self.clientes.append(cliente)

        logging.info("Cliente registrado: %s", cliente.nombre)

        return cliente

    # REGISTRAR SERVICIO

    def agregar_servicio(self, servicio):

        if not isinstance(servicio, Servicio):
            raise ErrorServicio("El objeto no corresponde a un servicio valido.")

        if any(s.identificacion == servicio.identificacion for s in self.servicios):
            raise ErrorServicio("El codigo del servicio ya existe.")

        self.servicios.append(servicio)

        logging.info("Servicio registrado: %s", servicio.nombre)

        return servicio

    # CREAR RESERVA

    def crear_reserva(self, documento, codigo_servicio, duracion):

        cliente = next(
            (c for c in self.clientes if c.identificacion == documento), None
        )

        servicio = next(
            (s for s in self.servicios if s.identificacion == codigo_servicio), None
        )

        if cliente is None:
            raise ErrorCliente("No se encontro el cliente solicitado.")

        if servicio is None:
            raise ErrorServicio("No se encontro el servicio solicitado.")

        reserva = Reserva(
            f"R{len(self.reservas) + 1:03d}",
            cliente,
            servicio,
            duracion
        )

        self.reservas.append(reserva)

        logging.info("Reserva creada: %s", reserva.identificacion)

        return reserva

    # BUSCAR RESERVA

    def buscar_reserva(self, codigo):

        reserva = next(
            (r for r in self.reservas if r.identificacion == codigo), None
        )

        if reserva is None:
            raise ErrorReserva("La reserva no existe.")

        return reserva

    # MOSTRAR CLIENTES

    def listar_clientes(self):

        print("\n========== LISTA DE CLIENTES ==========")

        if not self.clientes:
            print("No hay clientes registrados.")
            return

        for cliente in self.clientes:
            cliente.mostrar_informacion()

    # MOSTRAR SERVICIOS

    def listar_servicios(self):

        print("\n========== SERVICIOS DISPONIBLES ==========")

        if not self.servicios:
            print("No hay servicios registrados.")
            return

        for servicio in self.servicios:
            servicio.mostrar_informacion()
            print("Descripcion:", servicio.describir())
            print("Disponible:", "Si" if servicio.disponible else "No")

    # MOSTRAR RESERVAS

    def listar_reservas(self):

        print("\n========== LISTA DE RESERVAS ==========")

        if not self.reservas:
            print("No hay reservas registradas.")
            return

        for reserva in self.reservas:
            reserva.mostrar_informacion()


# ============================================================
# 11. REGISTRO DE ERRORES Y EVENTOS
# ============================================================

def ejecutar_operacion(descripcion, funcion):

    print("\nOPERACION:", descripcion)

    try:
        funcion()

    except ErrorSistema as error:
        logging.error("Error controlado: %s", error)
        print("Operacion no realizada:", error)

    except Exception:
        logging.exception("Error inesperado.")
        print("Se presento un error inesperado. El sistema continua.")

    else:
        logging.info("Operacion exitosa: %s", descripcion)
        print("Operacion realizada correctamente.")

    finally:
        print("Fin de la operacion.")


# ============================================================
# 12. PRUEBAS AUTOMATICAS: MINIMO 10 OPERACIONES
# ============================================================

def ejecutar_pruebas():

    print("\n==========================================")
    print("     PRUEBAS DEL SISTEMA SOFTWARE FJ")
    print("==========================================")

    sistema = SistemaSoftwareFJ(cargar_servicios=False)

    # OPERACION 1: Registro valido de cliente

    ejecutar_operacion(
        "Registro de cliente valido",
        lambda: sistema.registrar_cliente(
            "Carlos Perez", "123456789", "carlos@gmail.com", "3101234567"
        )
    )

    # OPERACION 2: Registro invalido de cliente

    ejecutar_operacion(
        "Registro de cliente con documento incorrecto",
        lambda: sistema.registrar_cliente(
            "Maria Lopez", "ABC123", "maria@gmail.com", "3001234567"
        )
    )

    # OPERACION 3: Creacion de servicio valido

    ejecutar_operacion(
        "Creacion de servicio de sala",
        lambda: sistema.agregar_servicio(
            ServicioSala("S01", "Sala principal", 5000)
        )
    )

    # OPERACION 4: Creacion de servicio invalido

    ejecutar_operacion(
        "Creacion de servicio con tarifa negativa",
        lambda: sistema.agregar_servicio(
            ServicioEquipo("E02", "Computador", -1000)
        )
    )

    # OPERACION 5: Registro de cliente duplicado

    ejecutar_operacion(
        "Registro de documento duplicado",
        lambda: sistema.registrar_cliente(
            "Carlos Perez", "123456789", "otro@gmail.com", "3101234567"
        )
    )

    # OPERACION 6: Creacion de reserva correcta

    ejecutar_operacion(
        "Creacion de reserva valida",
        lambda: sistema.crear_reserva("123456789", "S01", 3)
    )

    # OPERACION 7: Creacion de reserva incorrecta

    ejecutar_operacion(
        "Reserva con duracion incorrecta",
        lambda: sistema.crear_reserva("123456789", "S01", 0)
    )

    # OPERACION 8: Confirmacion de reserva

    ejecutar_operacion(
        "Confirmacion de reserva",
        lambda: sistema.buscar_reserva("R001").confirmar()
    )

    # OPERACION 9: Procesamiento y calculo de costo

    ejecutar_operacion(
        "Procesamiento de reserva con impuesto y descuento",
        lambda: sistema.buscar_reserva("R001").procesar(19, 10)
    )

    # OPERACION 10: Crear y cancelar una segunda reserva

    def crear_y_cancelar():
        reserva = sistema.crear_reserva("123456789", "S01", 2)
        reserva.cancelar()

    ejecutar_operacion(
        "Creacion y cancelacion de reserva",
        crear_y_cancelar
    )

    print("\n==========================================")
    print("       FIN DE LAS PRUEBAS")
    print("==========================================")

    sistema.listar_clientes()
    sistema.listar_servicios()
    sistema.listar_reservas()
