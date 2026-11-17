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
