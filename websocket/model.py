import re
from hashlib import sha1
from base64 import b64encode
import struct
import array

from . import settings


class WebSocketModel:
    client = {}

    def register_client(self, connection, address):
        self.client[connection] = {'address': address, 'accepted': False}

    def close_connection(self, connection):
        del self.client[connection]


    def accepted(self, connection):
        return self.client[connection]['accepted']

    def accept_connection(self, connection, request):
        answer = self.create_answer(request)
        connection.send(answer)
        self.client[connection]['accepted'] = True


    def create_answer(self, requested_key):
        requested_key += '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        requested_key = requested_key.encode()
        answer_key = b64encode( (sha1(requested_key)).digest() )

        answer = 'http/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: %s\r\n\r\n' % (answer_key.decode('utf-8'))
        return answer.encode()


    def get_websocket_key(self, request):
        delimeter = settings.regustrations_request_delimeter

        request = request.decode('utf-8')
        lines = request.split(delimeter)
        for line in lines:
            if re.match(r'Sec-WebSocket-Key', line):
                key = line.split(': ')
                return key[1]

    def is_close_connection_code(self, data):
        byte = struct.unpack_from('!BB', data)
        return byte == (136, 130) or byte == (136, 128)


    def process_browser_request(self, request):
        delimeter = settings.regustrations_request_delimeter

        request = request.decode()
        lines = request.split(delimeter)

        query = {}

        if settings.http_registrations_request:
            query['method'], query['app'], query['http'] = lines[0].split(' ')
            query['app'] = query['app'][1:]

        for line in lines:
            if re.search(':', line):
                name, value = line.split(': ', 1)
                query[name] = value


        return query


    def unpack_frame(self, data):
        frame = {}
        byte1, byte2 = struct.unpack_from('!BB', data)

        masked = (byte2 >> 7) & 1
        mask_offset = 4 if masked else 0

        offset, length = self.chech_hint(data, byte2)

        result = array.array('B')
        result.fromstring(data[offset + mask_offset:])

        if masked:
            mask_bytes = struct.unpack_from('!BBBB', data, offset)

            for i in range(len(result)):
                result[i] ^= mask_bytes[i % 4]

        return result.tostring()


    def chech_hint(self, data, byte):
        hint = byte & 0x7f
        if hint < 126:
            offset = 2
            length = hint

        if hint == 126:
            offset = 4
            length = struct.unpack_from('!H', data, 2)[0]

        if hint == 127:
            offset = 8
            length = struct.unpack_from('!Q', data, 2)[0]

        return offset, length


    def pack_frame(self, data):
        data = data.encode()
        b1 = 0x80 | (0x1 & 0x0f)

        length = len(data)

        if length <= 125:
            header = struct.pack('>BB', b1, length)

        if 125 < length < 65536:
            header = struct.pack('>BBH', b1, 126, length)

        if length >= 65536:
            header = struct.pack('>BBQ', b1, 127, length)

        return header + data
