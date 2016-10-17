import json

class ASCIITransportFormat:

    SUPPORTED_TYPES = ['FILE', 'JSON', 'STRING']

    def __init__(self, type=None, data=None, encoded:bool=False) -> None:
        """ASCIITransportFormat constructor.
        Parameters:
            type: can currently be 'FILE', 'JSON', or 'STRING', type of constructing data
            data: a filename, JSON string, or ASCII string, used to construct object
            encoded: bool that says whether the input data is encoded
        Returns: None
        """

        self.encoded = encoded
        self.pseudo_encode = False

        # return and call the correct functions depending on type
        if type and type.upper() in ASCIITransportFormat.SUPPORTED_TYPES:
            {
                'FILE': self._populate_with_filename,
                'JSON': self._populate_with_json,
                'STRING': self._populate_with_string,
            }.get(type.upper())(data)
        else:
            raise ValueError('Constructor used incorrectly.')

    def encode(self, force:bool=False) -> None:
        """Encode the current object's data.
        Parameters:
            force: Flag to prevent accidentally re-encoding, encoded data.
        Returns: None
        """

        if not force and self.encoded:
            raise ValueError('Cannot encode already encoded data. Trying setting the `force` flag if you believe your usage is correct. This may cause unexpected behavior.')
        else:
            encoded_result = ASCIITransportFormat.encode_data(self.data)
            if len(encoded_result) < len(self.data):
                self.data = encoded_result
                self.psuedo_encode = False
            else:
                self.pseudo_encode = True
            self.encoded = True

    def decode(self) -> None:
        """Decodes the current object's data.
        Parameters:
        Returns: None
        """

        if not self.encoded:
            raise ValueError('Cannot decode already decoded data.')
        elif not self.pseudo_encode:
            self.data = ASCIITransportFormat.decode_data(self.data)
        self.encoded = False
        self.pseudo_encode = False

    def encode_data(data:str) -> str:
        """Encodes a string and returns the result.
        Parameters:
            data: String to encode.
        Returns: The encoded string result.
        """

        if not data:
            return ''

        encoded_elements = []

        # FSM to implement encoding
        current_char, current_count = None, 0
        for char in data:
            if current_char == None:
                current_char = char
                current_count += 1
            elif current_char != char:
                encoded_elements.append(str(current_count)+current_char)
                current_char = char
                current_count = 1
            else:
                current_count += 1
        encoded_elements.append(str(current_count)+current_char)

        return ' '.join(encoded_elements)
    
    def decode_data(data:str) -> str:
        """Decodes an encoded string and returns the result.
        Parameters:
            data: Encoded data to decode.
        Returns: The decoded string result.
        """

        if not data:
            return ''
        
        decoded_string = ''

        # FSM to implement decoding
        space_seen = False
        current_element = ''
        for char in data:
            if space_seen and char != ' ':
                decoded_string += current_element[-2]*int(current_element[:-2])
                space_seen = False
                current_element = char
            else:
                current_element += char
                if char == ' ':
                    space_seen = True
        decoded_string += current_element[-1]*int(current_element[:-1])
        space_seen = False
        current_element = char

        return decoded_string

    def json(self) -> str:
        """Decodes an encoded string and returns the result.
        Parameters:
        Returns: String representing a JSON on object data.
        """

        return json.dumps(self.__dict__)
    
    def get_data(self) -> str:
        """Object data accessor.
        Parameters:
        Returns: The object's data.
        """

        return self.data

    def is_encoded(self) -> bool:
        """Object encoded flag accessor.
        Parameters:
        Returns: Whether the current data is encoded or not. 
        """

        return self.encoded

    def _populate_with_filename(self, data:str) -> None:
        """Private function populates object with data from a file.
        Parameters:
            data: File name.
        Returns: None
        """

        with open(data) as f:
            self.data = f.read()

    def _populate_with_json(self, data:str) -> None:
        """Private function populates object with data from a JSON.
        Parameters:
            data: String representing JSON.
        Returns: None.
        """

        new_data = json.loads(data)
        self._populate_with_dict(new_data)

    def _populate_with_dict(self, data:dict) -> None:
        """Private function populates object with data from a dict.
        Parameters:
            data: dict representing an ASCIITransportFormat's __dict__.
        Returns: None
        """

        self.data = data['data']
        self.encoded = data['encoded']

    def _populate_with_string(self, data:str) -> None:
        """Private function populates object with data from a string.
        Parameters:
            data: String to directly populate data with.
        Returns: None
        """

        self.data = data
