import socket
from time import localtime

def get_html():
    t = localtime()
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Pico Clock Config</title></head>
    <body style="background-color: rgb(40, 40, 40);">
        <h1 style="text-align:center">Pico Clock Configuration Portal</h1>
        <p style="text-align:center">Use this portal to configure your Pico Clock settings.</p>

        <form method="GET" action="/" style="text-align:center">
            <label for="timezone">Set New Time Zone Offset:</label><br>
            <input type="text" id="timezone_offset" name="timezone_offset" placeholder="e.g., -5"><br><br>
            <label for="brightnessDay">Set New Day Time Brightness:</label><br>
            <input type="text" id="brightness_day" name="brightness_day" placeholder="e.g., 20"><br><br>
            <label for="brightnessNight">Set New Night Time Brightness:</label><br>
            <input type="text" id="brightness_night" name="brightness_night" placeholder="e.g., 5"><br><br>
            <input type="submit" value="Update Setting">
        </form>

        <Time style="text-align:center">Current Time: {t[3]:02}:{t[4]:02}:{t[5]:02} (HH:MM:SS)</Time>

    </body>
    </html>
    """
    return html

def web_config():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print(f'Web Configuration Portal listening on {addr}')

    while True:
        try:
            cl, addr = s.accept()
            print(f'Client connected from {addr}')
            request = cl.recv(1024)
            # print(f'Request: {request}')
            if request.startswith(b'GET /?'):
                parse_settings(request)

            response = get_html()
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
        
        except Exception as e:
            print(f'Connection error: {e}')
        finally:
            cl.close()
            print('Connection closed')

config_Settings = ['timezone_offset', 'brightness_day', 'brightness_night']
def parse_settings(request):
    try:
        request_str = request.decode('utf-8')
        print(f'Parsing request: {request_str}')

        params = request_str.split(' ')[1][2:]  # Remove leading '/?'
        param_pairs = params.split('&')
        settings = {param.split('=')[0]: param.split('=')[1] for param in param_pairs}

        print(f'Parsing settings: {settings}')
        update_settings(settings)

    except Exception as e:
        print(f'Error parsing settings: {e}')

def update_settings(settings):
    try:
        for key, value in settings.items():
            if key in config_Settings:
                print(f'Updating setting {key} to {value}')
                globals()[key] = value
    except Exception as e:
        print(f'Error updating settings: {e}')