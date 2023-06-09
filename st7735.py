import time
import ustruct
import framebuf

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

    def pwron_init(self):
        self.init_gpio()
        self.reset()
        self.init()

    def reset(self):
        self.rst.on()
        time.sleep_ms(50)
        self.rst.off()
        time.sleep_ms(50)
        self.rst.on()
        time.sleep_ms(50)

    def init_gpio(self):
        self.rst.init(self.rst.OUT, None, value=1)
        #self.rst.init(self.rst.IN)
        self.rst.init(self.rst.OUT, value=1)
        self.cs.init(self.cs.OUT, None, value=1)
        #self.cs.init(self.cs.IN)
        self.cs.init(self.cs.OUT, value=1)
        self.rs.init(self.rs.OUT, None, value=0)
        #self.rs.init(self.rs.IN)
        self.rs.init(self.rs.OUT, value=1)

    def init(self):
        self._write_command(_SWRESET)
        time.sleep_ms(5)
        self.from_sleep()
        time.sleep_ms(50)
        for command, data in (
            (_FRMCTR1, b'\x01\x2c\x2d'),
            (_FRMCTR2, b'\x01\x2c\x2d'),
            (_FRMCTR3, b'\x01\x2c\x2d\x01\x2c\x2d'),
            (_INVCTR, b'0x07'),
            (_PWCTR1, b'\xa2\x02\x84'),
            (_PWCTR2, b'\xc5'),
            (_PWCTR3, b'\x0a\x00'),
            (_PWCTR4, b'\x8a\x2a'),
            (_PWCTR5, b'\x8a\xee'),
            (_VMCTR1, b'\x0e'),
            (_INVOFF, None),
            (_MADCTL, b'\xe8'),
            (_COLMOD, b'\x05'),
            (_CASET, b'\x00\x02\x00\x81'),
            (_RASET, b'\x00\x01\x00\xa0'),
            (_RAMWR, None),
            (_GMCTRP1, b'\x02\x1c\x07\x12\x37\x32\x29\x2d'
                       b'\x29\x25\x2b\x39\x00\x01\x03\x10'), # Gamma
            (_GMCTRN1, b'\x03\x1d\x07\x06\x2e\x2c\x29\x2d'
                       b'\x2e\x2e\x37\x3f\x00\x00\x02\x10'),
        ):
            self._write_command(command)
            if data: self._write_data(data)
        self._write_command(_NORON) # Normal display on
        time.sleep_ms(10)
        self.turn_on()
        time.sleep_ms(50)

    def turn_on(self):
        self._write_command(_DISPON)

    def turn_off(self):
        self._write_command(_DISPOFF)

    def to_sleep(self):
        self._write_command(_SLPIN)

    def from_sleep(self):
        self._write_command(_SLPOUT)

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
        caset = ustruct.pack(">HH", x0+0x01, x1+0x01)
        self._write_data(caset)
        self._write_command(_RASET)
        raset = ustruct.pack(">HH", y0+0x1a, y1+0x1a)
        self._write_data(raset)
        self._write_command(_RAMWR)
        if data:
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
        c = [x, y, x + w - 1, y + h - 1, None]
        #c.append(b'')
        self._write_block(*c)
        chunks, rest = divmod(w * h, 512)
        if chunks:
            data = ustruct.pack(">H", color) * 512
            for count in range(chunks):
                self._write_data(data)
        if rest:
            data = ustruct.pack(">H", color) * rest
            self._write_data(data)

    def fill(self, color):
        self.fill_rectangle(0, 0, self.width, self.height, color)

    def char(self, char, x, y, color=0xffff, background=0x0000):
        buffer = bytearray(8)
        framebuffer = framebuf.FrameBuffer1(buffer, 8, 8)
        framebuffer.text(char, 0, 0)
        color = ustruct.pack(">H", color)
        background = ustruct.pack(">H", background)
        data = bytearray(2 * 8 * 8)
        for c, byte in enumerate(buffer):
            for r in range(8):
                if byte & (1 << r):
                    data[r * 8 * 2 + c * 2] = color[0]
                    data[r * 8 * 2 + c * 2 + 1] = color[1]
                else:
                    data[r * 8 * 2 + c * 2] = background[0]
                    data[r * 8 * 2 + c * 2 + 1] = background[1]
        self._write_block(x, y, x + 7, y + 7, data)

    def char_from_buffer(self, buf, x, y, w=16, color=0xffff, background=0x0000):
        h = len(buf) / (w/8) * 2
        h = int(h)
        color = ustruct.pack(">H", color)
        background = ustruct.pack(">H", background)
        data = bytearray(w * h)
        for c, byte in enumerate(buf):
            for r in range(8):
                pos = c * w + r * 2
                if c % 1 == 1: r = r; pos += 8
                else: r = 7-r
                if byte & (1 << r):
                    data[pos] = color[0]
                    data[pos + 1] = color[1]
                else:
                    data[pos] = background[0]
                    data[pos + 1] = background[1]
        self._write_block(x, y, x + w-1, y + h-1, data)

    def text(self, text, x, y, color=0xffff, background=0x0000, wrap=None,
             vwrap=None, clear_eol=False):
        if wrap is None:
            wrap = self.width - 8
        if vwrap is None:
            vwrap = self.height - 8
        tx = x
        ty = y

        def new_line():
            nonlocal tx, ty

            tx = x
            ty += 8
            if ty >= vwrap:
                ty = y

        for char in text:
            if char == '\n':
                if clear_eol and tx < wrap:
                    self.fill_rectangle(tx, ty, wrap - tx + 7, 8, background)
                new_line()
            else:
                if tx >= wrap:
                    new_line()
                self.char(char, tx, ty, color, background)
                tx += 8
        if clear_eol and tx < wrap:
            self.fill_rectangle(tx, ty, wrap - tx + 7, 8, background)
        return tx+8
