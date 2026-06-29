#-----------------------------------------------------------------------#
# Software de gestión de servicios - FJ
#-----------------------------------------------------------------------#

import logging
 
logging.basicConfig(
    filename="eventos.log",
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
 
def registrar_evento(mensaje, es_error=False):
    if es_error == True:        
        logging.error(mensaje)
    if es_error == False:       
        logging.info(mensaje)
#-----------------------------------------------------------------------#
# Excepciones personalizadas para el software de gestión de servicios
#-----------------------------------------------------------------------#
class ErrorFJ(Exception):
    pass

#-----------------------------------------------------------------------#
# Validacion de datos y clases base para el software de gestión de servicios
#-----------------------------------------------------------------------#
from abc import ABC, abstractmethod
 
class EntidadBase(ABC):
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad
    @property
    def id_entidad(self):
        return self._id_entidad
    @abstractmethod
    def describir(self):
        pass
 
class Cliente(EntidadBase):
    def __init__(self, id_cliente, nombre, email):
        super().__init__(id_cliente)
        if nombre == "":        # <-- DEFECTO 3: solo revisa vacio,
            raise ErrorFJ("Nombre vacio")  #   no valida email ni espacios
        self._nombre = nombre
        self._email = email
    @property
    def nombre(self):
        return self._nombre
    @property
    def email(self):
        return self._email
    def describir(self):
        return "Cliente " + self._id_entidad + ": " + self._nombre

#-----------------------------------------------------------------------#
# Servicios y sus implementaciones para el software de gestión de servicios
#-----------------------------------------------------------------------#

class Servicio(EntidadBase):
    def __init__(self, id_servicio, nombre_servicio, costo_base):
        super().__init__(id_servicio)
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base
    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass
 
class ReservaSala(Servicio):
    def __init__(self, id_servicio, nombre_servicio, costo_base, capacidad):
        super().__init__(id_servicio, nombre_servicio, costo_base)
        self.capacidad = capacidad
    def calcular_costo(self, horas, descuento=0.0):
        # DEFECTO 4: no valida que horas > 0 (acepta negativos)
        total = (self.costo_base * horas) * (1 - descuento)
        return total
    def describir(self):
        return "Sala " + self.nombre_servicio
 
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre_servicio, costo_base, valor_seguro):
        super().__init__(id_servicio, nombre_servicio, costo_base)
        self.valor_seguro = valor_seguro
    def calcular_costo(self, dias, aplicar_seguro=False):
        total = self.costo_base * dias
        if aplicar_seguro == True:    # <-- tambien DEFECTO 1 (== True)
            total = total + self.valor_seguro
        return total
    def describir(self):
        return "Equipo " + self.nombre_servicio
 
class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre_servicio, costo_base, especialidad):
        super().__init__(id_servicio, nombre_servicio, costo_base)
        self.especialidad = especialidad
    def calcular_costo(self, horas, tarifa_urgencia=0.0):
        total = (self.costo_base * horas) + tarifa_urgencia
        return total
    def describir(self):
        return "Asesoria " + self.especialidad

#-----------------------------------------------------------------------#
# Clases de reserva y excepciones para el software de gestión de servicios
#-----------------------------------------------------------------------#

class Reserva(EntidadBase):
    def __init__(self, id_reserva, cliente, servicio, duracion):
        super().__init__(id_reserva)
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"     # <-- DEFECTO 5: atributo publico,
        self.costo_total = 0.0        #     sin proteccion (encapsulacion)
 
    def procesar_y_confirmar(self, **kwargs):
        try:                          # <-- DEFECTO 6: falta else y finally
            self.costo_total = self.servicio.calcular_costo(self.duracion, **kwargs)
            self.estado = "Confirmada"
            registrar_evento("Reserva " + self.id_entidad + " confirmada")
        except:                       # <-- DEFECTO 7: except pelado,
            registrar_evento("Error en reserva", True)  # sin tipo ni raise..from
 
    def cancelar(self):
        if self.estado == "Confirmada":
            self.costo_total = self.costo_total * 0.2
        self.estado = "Cancelada"
 
    def describir(self):
        return "Reserva " + self.id_entidad

#-----------------------------------------------------------------------#
# Simulaciones de casos de prueba para el software de gestión de servicios
#-----------------------------------------------------------------------#

clientes = []
servicios = []
reservas = []
 
print("SIMULACIONES")          # <-- DEFECTO 9: mensajes pobres
for caso in range(1, 11):
    print("Caso " + str(caso)) # <-- DEFECTO 8: sin try/except/else/finally
    if caso == 1:
        c = Cliente("C01", "Ingrith Toro", "ingrith@gmail.com")
        clientes.append(c)
        print(c.describir())
    elif caso == 2:
        try:
            c = Cliente("C02", "", "correo")
        except ErrorFJ:
            print("fallo cliente 2")
    elif caso == 3:
        s1 = ReservaSala("S01", "Sala VIP", 50000, 12)
        s2 = AlquilerEquipo("S02", "Proyector", 30000, 15000)
        servicios.append(s1)
        servicios.append(s2)
        print("servicios creados")
    elif caso == 4:
        s3 = AsesoriaEspecializada("S03", "Asesoria Ciber", 120000, "Sistemas")
        servicios.append(s3)
        print("asesoria creada")
    elif caso == 5:
        r = Reserva("R01", clientes[0], servicios[0], 4)
        r.procesar_y_confirmar(descuento=0.10)
        reservas.append(r)
        print("reserva: " + str(r.costo_total))
    elif caso == 6:
        r_err = Reserva("R02", clientes[0], servicios[2], -2)
        r_err.procesar_y_confirmar()   # acepta horas negativas (defecto 4)
        print("horas negativas: " + str(r_err.costo_total))
    elif caso == 7:
        r = reservas[0]
        r.cancelar()
        print("cancelada: " + str(r.costo_total))
    elif caso == 8:
        r = reservas[0]
        r.procesar_y_confirmar()   # reconfirma cancelada (no deberia)
        print("reconfirmar: " + r.estado)
    elif caso == 9:
        r_eq = Reserva("R03", clientes[0], servicios[1], 3)
        r_eq.procesar_y_confirmar(aplicar_seguro=True)
        reservas.append(r_eq)
        print("equipo: " + str(r_eq.costo_total))
    elif caso == 10:
        try:
            c_fail = Cliente("C10", "", "correo@fj.com")
        except ErrorFJ:
            print("fallo cliente 10")
#-----------------------------------------------------------------------#
# imprimimos fin
#-----------------------------------------------------------------------#
print("FIN")