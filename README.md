## Generador de Perfiles OpenVPN para MikroTik

Este script interactivo te ayuda a generar un archivo de perfil OpenVPN (`.ovpn`) para el servicio OpenVPN en dispositivos MikroTik. El perfil resultante se puede utilizar para configurar conexiones VPN seguras a través de tu dispositivo MikroTik.

### Requisitos

- Python 3.x instalado en tu sistema.

### Uso

1. Clona este repositorio`.

   ```bash
   git clone [https://github.com/tu_usuario/generador-openvpn-mikrotik.git](https://github.com/andresdrew02/OpenVPN-Mikrotik-Profile-Generator)
   ```

2. Navega al directorio donde se encuentra el script.

   ```bash
   cd OpenVPN-Mikrotik-Profile-Generator
   ```
   
2. Instala los requisitos necesarios.

   ```bash
   pip install -r requirements.txt
   ```
   
3. Ejecuta el script Python.

   ```bash
   python main
   ```

4. Sigue las instrucciones interactivas proporcionadas por el script. Proporciona la información necesaria cuando se te solicite (por ejemplo, IP del servidor OpenVPN, puerto, rutas de certificados, etc.).

5. Una vez que hayas completado la interacción, el script generará un archivo `.ovpn` que puedes utilizar con tu dispositivo MikroTik.

### Notas

- Asegúrate de tener acceso a los certificados y claves necesarios para configurar la conexión OpenVPN.
- Si experimentas algún problema o tienes alguna pregunta, no dudes en abrir un [issue](https://github.com/andresdrew02/OpenVPN-Mikrotik-Profile-Generator/issues) en este repositorio.

¡Disfruta de tu conexión segura con OpenVPN en tu dispositivo MikroTik!
