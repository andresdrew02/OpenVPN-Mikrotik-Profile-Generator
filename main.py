import re
import inquirer
import tkinter as tk
from tkinter import filedialog
from inquirer.themes import BlueComposure

class ConfigParameters:
    def __init__(self, protocol, remote, port, cipher, data_cipher, data_ciphers_fallback, auth_cipher):
        self.protocol = protocol
        self.remote = remote
        self.port = port
        self.cipher = cipher
        self.data_cipher = data_cipher
        self.data_ciphers_fallback = data_ciphers_fallback
        self.auth_cipher = auth_cipher
    
    def set_routes(self, ca_route, cert_route, key_route):
        self.ca_route = ca_route
        self.cert_route = cert_route
        self.key_route = key_route

    def __str__(self):
        return str(self.__dict__)

def questions():
    # Preguntamos primero la información que se debe de escribir, mas adelante pregunto las rutas de los certificados
    q = [
        inquirer.List("protocol", message="¿Que protocolo estás usando?", choices=["tcp", "udp"]),
        inquirer.Text("remote", message="¿Cual es la IP o dominio del servidor remoto?", validate=lambda _, x: re.match(r'^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$', x)),
        inquirer.Text("port", message="¿Cual es el puerto de destino? [1194]", validate=lambda _, x: re.match(r'^((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))$', x)),
        inquirer.List("cipher", message="¿Cual es el cifrado?", choices=["AES-256-GCM","AES-192-GCM","AES-128-GCM","AES-256-CBC","AES-192-CBC","AES-128-CBC, BLOWFISH"]),
        inquirer.List("data_cipher", message="¿Cual es el cifrado de la transmisión de datos? (Si no lo sabes, selecciona el cifrado anterior)", choices=["AES-256-GCM","AES-192-GCM","AES-128-GCM","AES-256-CBC","AES-192-CBC","AES-128-CBC", "BLOWFISH"]),
        inquirer.List("data_ciphers_fallback", message="¿Cual es el cifrado de respaldo? (Si no lo sabes, selecciona el cifrado anterior)", choices=["AES-256-GCM","AES-192-GCM","AES-128-GCM","AES-256-CBC","AES-192-CBC","AES-128-CBC", "BLOWFISH"]),
        inquirer.List("auth_cipher", message="¿Cual es el cifrado de autenticación?", choices=["SHA1","MD5", "NULL"]),
    ]

    # Preguntamos
    answers = inquirer.prompt(q, theme=BlueComposure())
    parameters = ConfigParameters(**answers)

    # Pedimos las rutas de los certificados
    print("Seleccione el certificado de la CA (.crt)")
    # Creamos una instancia de la clase Tk
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de la aplicación

    # Selecciona la CA
    ca_path = filedialog.askopenfilename()

    # Verificamos si se seleccionó un archivo
    if ca_path:
        print("Archivo seleccionado:", ca_path)
    else:
        print("Ningún archivo seleccionado, debe de seleccionar un archivo")
        exit()

    # Selecciona el certificado del cliente
    print("Seleccione el certificado del cliente (.crt)")
    client_cert_path = filedialog.askopenfilename()
     # Verificamos si se seleccionó un archivo
    if client_cert_path:
        print("Archivo seleccionado:", client_cert_path)
    else:
        print("Ningún archivo seleccionado, debe de seleccionar un archivo")
        exit()

    # Selecciona la privada del cliente
    print("Seleccione la clave privada del cliente (.key)")
    client_private_key = filedialog.askopenfilename()
     # Verificamos si se seleccionó un archivo
    if client_private_key:
        print("Archivo seleccionado:", client_private_key)
    else:
        print("Ningún archivo seleccionado, debe de seleccionar un archivo")
        exit()
    
    parameters.set_routes(ca_path, client_cert_path, client_private_key)
    return parameters

def generate_profile(config: ConfigParameters):
    # <<proto>>  <<server>> <<port>> <<ca>> <<cert>> <<key>> <<cipher>> <<data_cipher>> <<data_ciphers_fallback>> <<auth_cipher>>
    client = '''##############################################
# Sample client-side OpenVPN 2.0 config file #
# for connecting to multi-client server.     #
#                                            #
# This configuration can be used by multiple #
# clients, however each client should have   #
# its own cert and key files.                #
#                                            #
# On Windows, you might want to rename this  #
# file so it has a .ovpn extension           #
##############################################

# Specify that we are a client and that we
# will be pulling certain config file directives
# from the server.
client

# Use the same setting as you are using on
# the server.
# On most systems, the VPN will not function
# unless you partially or fully disable
# the firewall for the TUN/TAP interface.
;dev tap
dev tun

# Windows needs the TAP-Win32 adapter name
# from the Network Connections panel
# if you have more than one.  On XP SP2,
# you may need to disable the firewall
# for the TAP adapter.
;dev-node MyTap

# Are we connecting to a TCP or
# UDP server?  Use the same setting as
# on the server.
;proto tcp
proto <<proto>>

# The hostname/IP and port of the server.
# You can have multiple remote entries
# to load balance between the servers.
remote <<server>> <<port>>
;remote my-server-2 1194

# Choose a random host from the remote
# list for load-balancing.  Otherwise
# try hosts in the order specified.
;remote-random

# Keep trying indefinitely to resolve the
# host name of the OpenVPN server.  Very useful
# on machines which are not permanently connected
# to the internet such as laptops.
resolv-retry infinite

# Most clients don't need to bind to
# a specific local port number.
nobind

# Downgrade privileges after initialization (non-Windows only)
;user openvpn
;group openvpn

# Try to preserve some state across restarts.
persist-key
persist-tun

# If you are connecting through an
# HTTP proxy to reach the actual OpenVPN
# server, put the proxy server/IP and
# port number here.  See the man page
# if your proxy server requires
# authentication.
;http-proxy-retry # retry on connection failures
;http-proxy [proxy server] [proxy port #]

# Wireless networks often produce a lot
# of duplicate packets.  Set this flag
# to silence duplicate packet warnings.
;mute-replay-warnings

# SSL/TLS parms.
# See the server config file for more
# description.  It's best to use
# a separate .crt/.key file pair
# for each client.  A single ca
# file can be used for all clients.
<ca>
<<ca>>
</ca>
<cert>
<<cert>>
</cert>
<key>
<<key>>
</key>

# Verify server certificate by checking that the
# certificate has the correct key usage set.
# This is an important precaution to protect against
# a potential attack discussed here:
#  http://openvpn.net/howto.html#mitm
#
# To use this feature, you will need to generate
# your server certificates with the keyUsage set to
#   digitalSignature, keyEncipherment
# and the extendedKeyUsage to
#   serverAuth
# EasyRSA can do this for you.
remote-cert-tls server

# If a tls-auth key is used on the server
# then every client must also have the key.
#tls-auth ta.key 1
tls-client

# Select a cryptographic cipher.
# If the cipher option is used on the server
# then you must also specify it here.
# Note that v2.4 client/server will automatically
# negfotiate AES-256-GCM in TLS mode.
# See also the data-ciphers option in the manpage
cipher <<cipher>>
data-ciphers <<data_cipher>>
data-ciphers-fallback <<data_ciphers_fallback>>

# Enable compression on the VPN link.
# Don't enable this unless it is also
# enabled in the server config file.
#comp-lzo

# Set log file verbosity.
verb 4

# Silence repeating messages
;mute 20

auth <<auth_cipher>>
auth-nocache
redirect-gateway def1

auth-user-pass
'''

    final_config = client.replace('<<server>>', config.remote)
    if config.protocol == 'tcp':
        final_config = final_config.replace('<<proto>>', 'tcp-client')
    else:
        final_config = final_config.replace('<<proto>>', 'udp-client')
    final_config = final_config.replace('<<port>>', config.port == '' and '1194' or config.port)

    # Leemos el archivo de los certificados y de la clave privada y lo importamos en el config
    ca = open(config.ca_route, 'r')
    cert = open(config.cert_route, 'r')
    key = open(config.key_route, 'r')

    final_config = final_config.replace('<<ca>>', ca.read())
    final_config = final_config.replace('<<cert>>', cert.read())
    final_config = final_config.replace('<<key>>', key.read())
    ca.close()
    cert.close()
    key.close()

    final_config = final_config.replace('<<cipher>>', config.cipher)
    final_config = final_config.replace('<<data_cipher>>', config.data_cipher)
    final_config = final_config.replace('<<data_ciphers_fallback>>', config.data_ciphers_fallback)
    final_config = final_config.replace('<<auth_cipher>>', config.auth_cipher)

    return final_config

def save_file(config):
    # Selecciona la ruta a guardar el archivo
    file_path = filedialog.asksaveasfilename(defaultextension=".ovpn")
    f = open(file_path, 'w')
    f.write(config)
    f.close()

    saved_file = open(file_path, 'r')
    if saved_file.read() != '':
        print('[i] Se ha guardado el archivo, saliendo...')
        exit()
    else:
        print('[!] No se ha podido guardar el archivo, revise los permisos de lectura en la carpeta a guardar el archivo.')

def main():
    parameters = questions()
    config = generate_profile(parameters)
    save_file(config)


if __name__ == "__main__":
    main()