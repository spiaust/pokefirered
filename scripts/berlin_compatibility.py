"""The northern sign is the sole permitted change to older Berlin terrain."""
import struct
MARKER_INDEX=4*64+14

def before_route_marker(raw):
 assert len(raw)==64*44*2
 words=list(struct.unpack('<2816H',raw));assert words[MARKER_INDEX]==0x402
 words[MARKER_INDEX]=0x3165
 return struct.pack('<2816H',*words)
