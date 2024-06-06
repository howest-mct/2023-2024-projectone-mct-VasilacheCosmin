import socket
import json
import time

class GPSClient:
    def __init__(self, host="localhost", port=2947):
        self.host = host
        self.port = port
        self.gpsd_socket = None
        self.connect()

    def connect(self):
        try:
            self.gpsd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.gpsd_socket.connect((self.host, self.port))
            self.gpsd_socket.sendall(b'?WATCH={"enable":true,"json":true}\n')
            print("Connected to gpsd and listening for GPS data...")
        except Exception as e:
            print(f"Could not connect to gpsd: {e}")
            self.gpsd_socket = None

    def receive_data(self):
        if not self.gpsd_socket:
            print("Not connected to gpsd.")
            return None
        try:
            data = self.gpsd_socket.recv(4096)
            if data:
                return data.splitlines()
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

    def parse_data(self, data):
        gps_data = {"lat": None, "lon": None, "speed": None}
        for line in data:
            try:
                packet = json.loads(line)
                if packet.get('class') == 'TPV':  # TPV class has the position and velocity information
                    gps_data['lat'] = packet.get('lat', "N/A")
                    gps_data['lon'] = packet.get('lon', "N/A")
                    gps_data['speed'] = packet.get('speed', "N/A")
                    return gps_data
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
            except KeyError as e:
                print(f"Key error: {e}")
        return gps_data

    def run(self):
        try:
            while True:
                data = self.receive_data()
                if data:
                    gps_info = self.parse_data(data)
                    if gps_info:
                        print(gps_info)
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting...")
        except Exception as e:
            print(f"Got exception: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        if self.gpsd_socket:
            self.gpsd_socket.close()
            print("GPS socket closed.")

# Gebruik de GPSClient klasse in je main script
if __name__ == "__main__":
    gps_client = GPSClient()
    gps_client.run()
