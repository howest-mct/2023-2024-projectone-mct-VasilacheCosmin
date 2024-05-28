import spidev

class MCP3008:
    def __init__(self, bus=0, device=0, max_speed_hz=1350000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed_hz

    def read_adc(self, channel):
        # Controleer of kanaal binnen bereik is
        if channel < 0 or channel > 7:
            return -1
        
        # Maak een SPI bericht
        r = self.spi.xfer2([1, (8 + channel) << 4, 0])
        
        # Combineer de data en converteer naar 10-bit waarde
        adc_out = ((r[1] & 3) << 8) + r[2]
        return adc_out

    def close(self):
        self.spi.close()
