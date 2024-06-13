import logging
import math
import re
import sys

# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_pe import *
import grpc
from chirpstack_api.as_pb.external import api
# Importing the API exception
from tb_rest_client.rest import ApiException
import pandas
import configparser

print("Solar plant generator version: 1.8")

class DeviceChemik:
    campo = None
    eui = None
    power_station = None
    inversor = None
    caja_string = None
    n_chekness = None
    canal1 = None
    canal2 = None
    canal3 = None
    canal4 = None
    ubicacion = None
    fecha_hora = None
    token = None
    harness = None
    latitud = None
    longitud = None
    inactivityTimeout = None

    def __init__(self, campo, power_station, inversor, caja_string, eui,
                 canal1, canal2, canal3, canal4, ubicacion, fecha_hora, n_chekness, harness, latitud, longitud, inactivityTimeout):
        self.campo = campo
        self.power_station = power_station
        self.inversor = inversor
        self.caja_string = caja_string
        self.eui = eui
        self.canal1 = canal1
        self.canal2 = canal2
        self.canal3 = canal3
        self.canal4 = canal4
        self.ubicacion = ubicacion
        self.fecha_hora = fecha_hora
        self.n_chekness = n_chekness
        self.harness = harness
        self.latitud = latitud
        self.longitud = longitud
        self.inactivityTimeout = inactivityTimeout

    def set_campo(self, campo):
        self.campo = campo
    def set_power_station(self, power_station):
        self.power_station = power_station
    def set_caja_string(self, caja_string):
        self.caja_string = caja_string
    def set_eui(self, eui):
        self.eui = eui
    def set_canal1(self, canal1):
        self.canal1 = canal1
    def set_canal2(self, canal2):
        self.canal2 = canal2
    def set_canal3(self, canal3):
        self.canal3 = canal3
    def set_canal4(self, canal4):
        self.canal4 = canal4
    def set_ubicacion(self, ubicacion):
        self.ubicacion = ubicacion
    def set_fecha_hora(self, fecha_hora):
        self.fecha_hora = fecha_hora
    def set_inversor(self, inversor):
        self.inversor = inversor
    def set_n_chekness(self, n_chekness):
        self.n_chekness = n_chekness
    def set_token(self, token):
        self.token = token
    def set_longitud(self, longitud):
        self.longitud = longitud
    def set_harness(self, harness):
        self.harness = harness
    def set_latitud(self, latitud):
        self.latitud = latitud
    def set_inactivityTimeout(self, inactivityTimeout):
        self.inactivityTimeout = inactivityTimeout

    def get_campo(self):
        return self.campo
    def get_power_station(self):
        return self.power_station
    def get_caja_string(self):
        return self.caja_string
    def get_inversor(self):
        return self.inversor
    def get_eui(self):
        return self.eui
    def get_canal1(self):
        return self.canal1
    def get_canal2(self):
        return self.canal2
    def get_canal3(self):
        return self.canal3
    def get_canal4(self):
        return self.canal4
    def get_ubicacion(self):
        return self.ubicacion
    def get_fecha_hora(self):
        return self.fecha_hora
    def get_n_chekness(self):
        return self.n_chekness
    def get_Token(self):
        return self.token
    def get_harness(self):
        return self.harness
    def get_latitud(self):
        return self.latitud
    def get_longitud(self):
        return self.longitud
    def get_inactivityTimeout(self):
        return self.inactivityTimeout

def getExistentDevices():
    # The API token (retrieved using the web-interface).
    global api_token
    # Connect without using TLS.
    try:
        channel = grpc.insecure_channel(chirpstack_server)

        client = api.ApplicationServiceStub(channel)

        # Define the API key meta-data.
        auth_token = [("authorization", "Bearer %s" % api_token)]

        # Construct request.
        device = api.ListApplicationRequest()
        device.limit = device_limit;

        resp = client.List(device, metadata=auth_token)

        existent_devices = list()
        for application in resp.result:
            # Device-queue API client.
            client = api.DeviceServiceStub(channel)

            # Define the API key meta-data.
            auth_token = [("authorization", "Bearer %s" % api_token)]

            # Construct request.
            device = api.ListDeviceRequest()
            device.application_id = application.id
            device.limit = device_limit;

            resp = client.List(device, metadata=auth_token)

            # Print the downlink frame-counter value.
            for device in resp.result:
                existent_devices.append([device.dev_eui, device.application_id, device.device_profile_id])

        return existent_devices
    except Exception as e:
        print("Problemas al conectar con chirpstack")
        print(e)
        exit(1)


def updateDevice(eui, dev_profile, app_id, token):
    # The API token (retrieved using the web-interface).
    global api_token
    # Connect without using TLS.
    try:
        channel = grpc.insecure_channel(chirpstack_server)
        # Device-queue API client.
        client = api.DeviceServiceStub(channel)

        # Define the API key meta-data.
        auth_token = [("authorization", "Bearer %s" % api_token)]

        # Construct request.
        device = api.UpdateDeviceRequest()
        device.device.dev_eui = eui
        device.device.name = eui
        device.device.application_id = app_id
        device.device.device_profile_id = dev_profile
        device.device.skip_f_cnt_check = True
        device.device.variables['ThingsBoardAccessToken'] = token
        device.device.description = "Lo cree automaticamente"

        resp = client.Update(device, metadata=auth_token)
    except Exception as e:
        print("Fallo en la conexion con Chirpstack updating devices")
        print(e)
        exit(1)

def activateIntegration(app_id, server):
    # The API token (retrieved using the web-interface).
    global api_token
    # Connect without using TLS.
    try:
        channel = grpc.insecure_channel(chirpstack_server)

        # Device-queue API client.
        client = api.ApplicationServiceStub(channel)

        # Define the API key meta-data.
        auth_token = [("authorization", "Bearer %s" % api_token)]

        # Construct request.
        integration = api.CreateThingsBoardIntegrationRequest ()
        integration.integration.server  = server
        integration.integration.application_id = app_id

        resp = client.CreateThingsBoardIntegration(integration, metadata=auth_token)
    except Exception as e:
        print("Fallo en la conexion con Chirpstack creating integration")
        print(e)
        exit(1)

def getActiveIntegration(app_id):
    # The API token (retrieved using the web-interface).
    global api_token
    # Connect without using TLS.
    channel = grpc.insecure_channel(chirpstack_server)
    # Device-queue API client.
    client = api.ApplicationServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Construct request.
    integration = api.GetThingsBoardIntegrationRequest ()
    integration.application_id = app_id

    return client.GetThingsBoardIntegration(integration, metadata=auth_token).integration.application_id == app_id

config_aux = configparser.ConfigParser()
try:
    config_aux.read('config.ini')
except Exception as e:
    print(e)
    exit(1)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# ThingsBoard REST API URL
thingsboard_server = config_aux['CONFIG']['thingsboard_server']
chirpstack_server = config_aux['CONFIG']['chirpstack_server']
# Default Tenant Administrator credentials
username = config_aux['CONFIG']['username']
password = config_aux['CONFIG']['password']
api_token = config_aux['CONFIG']['api_token']
device_profile_id = config_aux['CONFIG']['device_profile_id']
device_limit = int(config_aux['CONFIG']['device_limit'])
def chirpstack_device_creation(devices, option):
    for eui, dev_profile, app_id in devices:
        updateDevice(eui, dev_profile, app_id)


def parse_assets(devices):
    list_assets_pws = []
    # se buscan los diferentes power stations
    asset = devices[devices.columns[1]][0]
    list_assets_pws.append(asset)
    for asset1 in devices[devices.columns[1]][:]:
        if asset1 != asset:
            list_assets_pws.append(asset1)
            asset = asset1
    list_assets_inv = []
    # se busca los diferentes inversores
    asset = devices[devices.columns[2]][0]
    list_assets_inv.append(asset)
    for asset1 in devices[devices.columns[2]][:]:
        if asset1 != asset:
            list_assets_inv.append(asset1)
            asset = asset1
    list_assets_cs = []
    # se busca los diferentes strings
    asset = devices[devices.columns[3]][0]
    if math.isnan(asset):
        asset = 0.0
    list_assets_cs.append(asset)
    for asset1 in devices[devices.columns[3]][:]:
        if math.isnan(asset1):
            asset1 = 0.0
        if asset1 != asset:
            list_assets_cs.append(asset1)
            asset = asset1

    return list_assets_pws, list_assets_inv, list_assets_cs

def set_attributes(devices, device):
    if devices[devices.columns[0]][device] == "":
        campo = "NaN"
    else:
        campo = devices[devices.columns[0]][device]
    if math.isnan(devices[devices.columns[1]][device]):
        power_station = "NaN"
    else:
        power_station = int(devices[devices.columns[1]][device])
    if math.isnan(devices[devices.columns[2]][device]):
        inversor = "NaN"
    else:
        inversor = int(devices[devices.columns[2]][device])
    if math.isnan(devices[devices.columns[3]][device]):
        inactivityTimeout = "NaN"
    else:
        inactivityTimeout = int(devices[devices.columns[3]][device])
    if math.isnan(devices[devices.columns[4]][device]):
        caja_string = "NaN"
    else:
        caja_string = int(devices[devices.columns[4]][device])
    if devices[devices.columns[5]][device] == "":
        eui = "NaN"
    else:
        eui = devices[devices.columns[5]][device]
    if devices[devices.columns[6]][device] == "":
        n_chekness = "NA"
    else:
        n_chekness = str(devices[devices.columns[6]][device])
    if math.isnan(devices[devices.columns[7]][device]):
        harness = "NaN"
    else:
        harness = int(devices[devices.columns[7]][device])
    if math.isnan(devices[devices.columns[8]][device]):
        canal1 = "NA"
    else:
        canal1 = int(devices[devices.columns[8]][device])
    if math.isnan(devices[devices.columns[9]][device]):
        canal2 = "NaN"
    else:
        canal2 = int(devices[devices.columns[9]][device])
    if math.isnan(devices[devices.columns[10]][device]):
        canal3 = "NaN"
    else:
        canal3 = int(devices[devices.columns[10]][device])
    if math.isnan(devices[devices.columns[11]][device]):
        canal4 = "NaN"
    else:
        canal4 = int(devices[devices.columns[11]][device])
    print(devices[devices.columns[11]][device])
    if devices[devices.columns[12]][device] == "":
        ubicacion = "NaN"
        latitud = "NaN"
        longitud = "NaN"
    elif isinstance(devices[devices.columns[12]][device], float) or isinstance(devices[devices.columns[11]][device], int):
        if math.isnan(devices[devices.columns[12]][device]):
            ubicacion = "NaN"
            latitud = "NaN"
            longitud = "NaN"
    else:
        ubicacion = devices[devices.columns[12]][device]
        latitud = devices[devices.columns[12]][device].split(', ')[0]
        longitud = devices[devices.columns[12]][device].split(', ')[1]
    if isinstance(devices[devices.columns[13]][device], float):
        fecha_hora = "NaN"
    else:
        fecha_hora = devices[devices.columns[13]][device]
    
    return [campo, power_station, inversor, inactivityTimeout, caja_string, eui, \
        canal1, canal2, canal3, canal4, ubicacion, fecha_hora, n_chekness, harness, latitud, longitud]

def parse_devices(devices):
    list_devices = []
    for device in devices.index:
        attributes = set_attributes(devices, device)
        list_devices.append(DeviceChemik(attributes[0], attributes[1], attributes[2], attributes[3], attributes[4],
                 attributes[5], attributes[6], attributes[7], attributes[8], attributes[9], attributes[10],
                                         attributes[11], attributes[12], attributes[13], attributes[14], attributes[15]))
    return list_devices


def encuentra_dispositivo(d_existent, list):
    encontrado = False
    i = 0
    for d in list:
        if d.get_eui() == d_existent:
            encontrado = True
            break
        i+=1
    return encontrado, i


def create_customer(customerName, rest_client, option, client_id, devicesData):
    customer = Customer(title=customerName)
    try:
        customer = rest_client.save_customer(body=customer)
    except Exception as e:
        print("El cliente ya existe")
        if option == "-u":
            try:
                customer = rest_client.get_customer_by_id(CustomerId(client_id, "CUSTOMER"))
                if customer.name != customerName:
                    print("El campo proporcionado en el csv no coincide")
                    exit(1)
            except Exception as e:
                print("Comprobar que el id del cliente es correcto")
                print(e)
                exit(1)
        if option == "-f":
            try:
                customer = rest_client.get_customer_by_id(CustomerId(client_id, "CUSTOMER"))
                print(customer)
                if customer.name != customerName:
                    print("El campo proporcionado en el csv no coincide")
                    exit(1)
                resp = rest_client.get_customer_devices(customer.id, 1, 0)
                if resp.data:
                    resp = rest_client.get_customer_devices(customer.id, resp.total_pages, 0)
                    print(resp)
                    for z in range(0, resp.total_elements):
                        existe = False
                        for d in devicesData:
                            if resp.data[z].name == d.get_eui():
                                existe = True
                        if existe == False:
                            device = resp.data[z]
                            rest_client.delete_device(device.id)
                            print("Elimino")
            except Exception as e:
                print("Problemas en la eliminacion del usuario")
                print(e)
                exit(1)
    return customer


def create_device(d, customer, rest_client, devicesData, i, option):
    device = Device(name=d.get_eui(), type='default',
                    device_profile_id=DeviceProfileId(device_profile_id, 'DEVICE_PROFILE'),
                    owner_id=customer.id,
                    customer_id=customer.id, tenant_id=customer.owner_id)
    try:
        device = rest_client.save_device(device)
        print("Created device " + d.get_eui())
        devicesData[i].set_token(rest_client.get_device_credentials_by_device_id(device.id).credentials_id)
        devicesData[i] = devicesData[i]
        i += 1
    except Exception as e:
        print("Ya existe el dispositivo")
        print(d.get_eui())
        print(e)
        if option == "-u" or option == "-f":
            try:
                resp = rest_client.get_customer_devices(customer.id, 1, 0)
                resp = rest_client.get_customer_devices(customer.id, resp.total_pages, 0)
            except Exception as e:
                print("Fallo a la hora de recuperar los dispositivos para un cliente")
                print(e)
                exit(1)
            for z in range(0, resp.total_elements + 1):
                if resp.data[z].name == d.get_eui():
                    print("Updated device " + d.get_eui())
                    device = resp.data[z]
                    devicesData[i].set_token(rest_client.get_device_credentials_by_device_id(device.id).credentials_id)
                    devicesData[i] = devicesData[i]
                    i+=1
                    break
    return device, i, devicesData


def update_attributes(devicesData, device, d, option, rest_client, i):
    if option != "-m" or (devicesData[i - 1].get_Token() is not None and option == "-m"):
        # save device shared attributes
        json = {'eui': d.get_eui(),
                'campo': d.get_campo(),
                'inversor': d.get_inversor(),
                'caja string': d.get_caja_string(),
                'N chekness': d.get_n_chekness(),
                'canal 1': d.get_canal1(),
                'canal 2': d.get_canal2(),
                'canal 3': d.get_canal3(),
                'canal 4': d.get_canal4(),
                'ubicacion': d.get_ubicacion(),
                'fecha hora': d.get_fecha_hora(),
                'power station': d.get_power_station(),
                'harness': d.get_harness(),
                'latitude': d.get_latitud(),
                'longitude': d.get_longitud(),
                'inactivityTimeout': d.get_inactivityTimeout()}
        print(device.id)
        try:
            rest_client.save_device_attributes(DeviceId(device.id, 'DEVICE'), 'SERVER_SCOPE', json)
        except Exception as e:
            print("Fallo a la hora de actualizar los dispositivos")
            print(e)
            exit(1)


def sincronizar_chirpstack(devicesData):
    existent_devices = getExistentDevices()
    for existent_device in existent_devices:
        encontrado, i = encuentra_dispositivo(existent_device[0], devicesData)
        if encontrado and devicesData[i].get_Token() is not None:
            try:
                found = getActiveIntegration(existent_device[1])
                if found:
                    print("Actualizo Chirpstack")
                    updateDevice(existent_device[0], existent_device[2], existent_device[1], devicesData[i].get_Token())
            except Exception as e:
                print(e)
                try:
                    activateIntegration(existent_device[1], thingsboard_server)
                    print("Integro Chirpstack")
                    updateDevice(existent_device[0], existent_device[2], existent_device[1], devicesData[i].get_Token())
                    print("Actualizo Chirpstack")
                except Exception as e:
                    print("Error a la hora incorporar integracion")
                    print(e)
        elif not encontrado:
            print("El dispositivo: " + existent_device[0] + " no se ha encontrado en la lista de añadidos a ThingsBoard")


def thingsboard_device_creation(devices, option, client_id):
    customerName = devices[devices.columns[0]][0]
    assets = parse_assets(devices)
    devicesData = parse_devices(devices)

    with RestClientPE(base_url=thingsboard_server) as rest_client:
        try:
            rest_client.login(username=username, password=password)
        except Exception as e:
            print("Fallo al hacer login, comprobar credenciales")
            exit(1)

        customer = create_customer(customerName, rest_client, option, client_id, devicesData)
        i = 0
        for d in devicesData:
            # creating a Device
            device, i, devicesData = create_device(d, customer, rest_client, devicesData, i, option)

            update_attributes(devicesData, device, d, option, rest_client, i)

    sincronizar_chirpstack(devicesData)



def check_only_client(devices):

    customer = devices[devices.columns[0]][0]
    iguales = True
    for device in devices.index:
        if devices[devices.columns[0]][device] != customer:
            iguales = False
            print("Encontrado dos campos: " + devices[devices.columns[0]][device] + " y " + customer)
            print("Solo debe de haber uno")
            break

    return iguales


def check_eui_vacia(devices):
    correcto = True
    for device in devices.index:
        if devices[devices.columns[5]][device] == "":
            correcto = False
            print("Encontrado eui vacio en la fila " + str(device+1))
            print("No puede ser vacio")
            break
    return correcto

def check_eui_formato(devices):
    correcto = True
    for device in devices.index:
        s = devices[devices.columns[5]][device]
        if not (re.match("^[A-Za-z0-9]*$", s)) and len(s) != 16:
            correcto = False
            print("Encontrado eui con formato no valido en fila " + str(device+1))
            print("No puede tener este fomato")
            break
    return correcto

def check_eui_repetida(devices):
    correcto = True
    for device in devices.index[0:]:
        eui_aux = devices[devices.columns[5]][device]
        for device_aux in devices.index[device+1:]:
            if devices[devices.columns[5]][device_aux] == eui_aux:
                correcto = False
                print("Encontrado eui repetida en la fila " + str(device+1) + "eui " + eui_aux)
                print("No puede haber dos filas con misma eui")
                break

        if not correcto:
            break
    return correcto


def check_only_device(devices):

    correcto = check_eui_vacia(devices)
    if correcto:
        correcto = check_eui_formato(devices)
    if correcto:
        correcto = check_eui_repetida(devices)

    return correcto


def check_devices(devices):
    if not check_only_client(devices):
        return False
    elif not check_only_device(devices):
        return False
    else:
        return True

flags = sys.argv[1:]

if not flags:
    print("El uso del bebe programa debe de ser el siguiente:")
    print("python device_creation.py [-m] [fichero.csv] -> opción de crear csv TB")
    print("python device_creation.py [-u] [fichero.csv] -> opción de actualizar csv TB")
    print("python device_creation.py [-f] [fichero.csv] -> opción de sincronizacion csv TB")
    print("Esta ultima opción si se añade -f forzará que en TB esten tan solo los dispositivos del fichero csv.")
    exit()

if flags[0]!="-m" and flags[0]!="-u" and flags[0]!="-f":
    print("El uso del bebe programa debe de ser el siguiente:")
    print("python device_creation.py [-m] [fichero.csv] -> opción de crear csv TB")
    print("python device_creation.py [-u] [fichero.csv] -> opción de actualizar csv TB")
    print("python device_creation.py [-f] [fichero.csv] -> opción de sincronizacion csv TB")
    print("Esta ultima opción si se añade -f forzará que en TB esten tan solo los dispositivos del fichero csv.")
    exit()

if len(flags) < 2:
    print("El uso del bebe programa debe de ser el siguiente:")
    print("python device_creation.py [-m] [fichero.csv] -> opción de crear csv TB")
    print("python device_creation.py [-u] [fichero.csv] -> opción de actualizar csv TB")
    print("python device_creation.py [-f] [fichero.csv] -> opción de sincronizacion csv TB")
    print("Esta ultima opción si se añade -f forzará que en TB esten tan solo los dispositivos del fichero csv.")
    print("El uso del baba programa debe de ser el siguiente:")
    exit()

if flags[0] == "-m" and ".csv" in flags[1] and len(flags)==2:
    print("Opción de sincronización elegida se procede, a actualizar Chirpstack con json proporcionado.")
    devices = pandas.read_csv(flags[1], delimiter=";")
    devices = devices.drop(devices.columns[0], axis=1)
    if not check_devices(devices):
        exit(1)
    thingsboard_device_creation(devices, flags[0], "")
elif flags[0] == "-u" and ".csv" in flags[1] and len(flags)==3:
    print("Opción de sincronización elegida se procede, a actualizar Chirpstack con json proporcionado.")
    devices = pandas.read_csv(flags[1], delimiter=";")
    devices = devices.drop(devices.columns[0], axis=1)
    if not check_devices(devices):
        exit(1)
    thingsboard_device_creation(devices, flags[0], flags[2])
elif flags[0] == "-f" and ".csv" in flags[1] and len(flags)==3:
    print("Opción de sincronización elegida se procede, a actualizar Chirpstack con json proporcionado.")
    devices = pandas.read_csv(flags[1], delimiter=";")
    devices = devices.drop(devices.columns[0], axis=1)
    if not check_devices(devices):
        exit(1)
    thingsboard_device_creation(devices, flags[0], flags[2])
else:
    print("El uso del bebe programa debe de ser el siguiente:")
    print("python device_creation.py [-s] [fichero.json] -> opción de sincronización json Chirpstack")
    print("python device_creation.py [-add] [-f] [fichero.json] -> opción de añadir json Chirpstack")
    print("Esta ultima opción si se añade -f forzará aunque existan los dipositivos a que sean actualizados.")
    exit()


print("Proceso finalizado")
