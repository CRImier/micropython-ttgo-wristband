import time
import ustruct


_NOP=const(0x00)
_SWRESET=const(0x01)
_RDDID=const(0x04)
_RDDST=const(0x09)

_SLPIN=const(0x10)
_SLPOUT=const(0x11)
_PTLON=const(0x12)
_NORON=const(0x13)

_INVOFF=const(0x20)
_INVON=const(0x21)
_DISPOFF=const(0x28)
_DISPON=const(0x29)
_CASET=const(0x2A)
_RASET=const(0x2B)
_RAMWR=const(0x2C)
_RAMRD=const(0x2E)

_PTLAR=const(0x30)
_COLMOD=const(0x3A)
_MADCTL=const(0x36)

_FRMCTR1=const(0xB1)
_FRMCTR2=const(0xB2)
_FRMCTR3=const(0xB3)
_INVCTR=const(0xB4)
_DISSET5=const(0xB6)

_PWCTR1=const(0xC0)
_PWCTR2=const(0xC1)
_PWCTR3=const(0xC2)
_PWCTR4=const(0xC3)
_PWCTR5=const(0xC4)
_VMCTR1=const(0xC5)

_RDID1=const(0xDA)
_RDID2=const(0xDB)
_RDID3=const(0xDC)
_RDID4=const(0xDD)

_PWCTR6=const(0xFC)

_GMCTRP1=const(0xE0)
_GMCTRN1=const(0xE1)


class ST7735:
    """
    A simple driver for the ST7735-based displays.

    >>> from machine import Pin, SPI
    >>> import st7735
    >>> spi = SPI(miso=Pin(12), mosi=Pin(13, Pin.OUT), sck=Pin(14, Pin.OUT))
    >>> display = st7735.ST7735(128, 128, spi, Pin(2), Pin(4), Pin(5))
    >>> display.fill(0x7521)
    >>> display.pixel(64, 64, 0)

    """

    def __init__(self, width, height, spi, cs, rs, rst):
        self.width = width
        self.height = height
        self.spi = spi
        self.cs = cs
        self.rs = rs
        self.rst = rst
        self.cs.init(self.cs.OUT, value=1)
        self.rs.init(self.rs.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.reset()
        self.init()

    def reset(self):
        self.rst.on()
        time.sleep_ms(50)
        self.rst.off()
        time.sleep_ms(50)
        self.rst.on()
        time.sleep_ms(50)

    def init(self):
        self._write_command(_SWRESET)
        time.sleep_ms(5)
        self._write_command(_SLPOUT)
        time.sleep_ms(50)
        for command, data in (
            (_COLMOD, b'\x05'), # 16bit color
            # fastest refresh, 6 lines front porch, 3 line back porch
            (_FRMCTR1, b'\x00\x06\x03'),
            (_MADCTL, b'\x08'), # bottom to top refresh
            # 1 clk cycle nonoverlap, 2 cycle gate rise, 3 sycle osc equalie,
            # fix on VTL
            (_DISSET5, b'\x15\x02'),
            (_INVCTR, b'0x00'), # line inversion
            (_PWCTR1, b'\x02\x70'), # GVDD = 4.7V, 1.0uA
            (_PWCTR2, b'\x05'), # VGH=14.7V, VGL=-7.35V
            (_PWCTR3, b'\x01\x02'), # Opamp current small, Boost frequency
            (_VMCTR1, b'\x3c\x38'), # VCOMH = 4V, VOML = -1.1V
            (_PWCTR6, b'\x11\x15'),
            (_GMCTRP1, b'\x09\x16\x09\x20\x21\x1b\x13\x19'
                       b'\x17\x15\x1e\x2b\x04\x05\x02\x0e'), # Gamma
            (_GMCTRN1, b'\x08\x14\x08\x1e\x22\x1d\x18\x1e'
                       b'\x18\x1a\x24\x2b\x06\x06\x02\x0f'),
            (_CASET, b'\x00\x02\x00\x81'), # XSTART = 2, XEND = 129
            (_RASET, b'\x00\x02\x00\x81'), # XSTART = 2, XEND = 129
        ):
            self._write_command(command)
            self._write_data(data)
        self._write_command(_NORON) # Normal display on
        time.sleep_ms(1)
        self._write_command(_DISPON) # Screen on
        time.sleep_ms(50)

    def _write_command(self, command):
        self.rs.off()
        self.cs.off()
        self.spi.write(bytearray([command]))
        self.cs.on()

    def _write_data(self, data):
        self.rs.on()
        self.cs.off()
        self.spi.write(data)
        self.cs.on()

    def _write_block(self, x0, y0, x1, y1, data):
        self._write_command(_CASET)
        self._write_data(ustruct.pack(">HH", x0, x1))
        self._write_command(_RASET)
        self._write_data(ustruct.pack(">HH", y0, y1))
        self._write_command(_RAMWR)
        self._write_data(data)

    def pixel(self, x, y, color):
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return
        self._write_block(x, y, x, y, ustruct.pack(">H", color))

    def fill_rectangle(self, x, y, w, h, color):
        x = min(self.width - 1, max(0, x))
        y = min(self.height - 1, max(0, y))
        w = min(self.width - x, max(1, w))
        h = min(self.height - y, max(1, h))
        self._write_block(x, y, x + w - 1, y + h - 1, b'')
        chunks, rest = divmod(w * h, 512)
        if chunks:
            data = ustruct.pack(">H", color) * 512
            for count in range(chunks):
                self._write_data(data)
        data = ustruct.pack(">H", color) * rest
        self._write_data(data)

    def fill(self, color):
        self.fill_rectangle(0, 0, self.width, self.height, color)

