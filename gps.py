import socket
import json
import time

def main():
    try:
        # Connect to the gpsd daemon
        gpsd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gpsd_socket.connect(("localhost", 2947))
        gpsd_socket.sendall(b'?WATCH={"enable":true,"json":true}\n')
        
        print("Listening for GPS data on port 2947...")
        
        while True:
            try:
                data = gpsd_socket.recv(4096)
                if data:
                    for line in data.splitlines():
                        packet = json.loads(line)
                        if packet.get('class') == 'TPV':  # TPV class has the position and velocity information
                            lat = packet.get('lat', "N/A")
                            lon = packet.get('lon', "N/A")
                            speed = packet.get('speed', "N/A")
                            print(f"Latitude: {lat}, Longitude: {lon}, Speed: {speed} m/s")
                time.sleep(1)
                    
            except json.JSONDecodeError:
                # Handle JSON decoding error if data is incomplete or malformed
                pass
            except KeyError:
                # KeyError might occur if a key doesn't exist in the report
                pass
            except KeyboardInterrupt:
                # Gracefully handle user interruption
                print("\nProgram interrupted by user. Exiting...")
                break
            except Exception as e:
                # Handle other exceptions
                print(f"Got exception: {e}")
                break
                
    except Exception as e:
        print(f"Could not connect to gpsd: {e}")

if __name__ == "__main__":
    main()
