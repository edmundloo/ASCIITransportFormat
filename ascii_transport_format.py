import json

class ASCIITransportFormat:
    SUPPORTED_TYPES = ['FILE', 'JSON', 'STRING']

    def __init__(self, type=None, data=None, encoded:bool=False) -> None:
        """ASCIITransportFormat constructor.
        Parameters:
            type: can currently be 'FILE', 'JSON', or 'STRING', type of
                  constructing data
            data: a filename, JSON string, or ASCII string, used to
                  construct object
            encoded: bool that says whether the input data is encoded
        Returns: None
        """
        # initialize needed object flags
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
            raise ValueError(
                'Cannot encode already encoded data. Trying setting the '
                '`force` flag if you believe your usage is correct. '
                'This may cause unexpected behavior.'
            )
        else:
            # encode the actual data and record the result
            encoded_result = ASCIITransportFormat.encode_data(self.data)
            if len(encoded_result) < len(self.data):
                # if actually compressed, then use compressed version
                # which is not pseudo encoded
                self.data = encoded_result
                self.psuedo_encode = False
            else:
                # if compression is larger than original, don't use the larger
                # version and enable pseudo encoding
                self.pseudo_encode = True
            # set encoded flag if this function was run
            self.encoded = True

    def decode(self) -> None:
        """Decodes the current object's data.
        Parameters:
        Returns: None
        """

        if not self.encoded:
            raise ValueError('Cannot decode already decoded data.')
        elif not self.pseudo_encode:
            # only run decode if not pseudo encoded
            self.data = ASCIITransportFormat.decode_data(self.data)
        # reset *encoded flags since this is now decoded
        self.encoded = False
        self.pseudo_encode = False

    def encode_data(data:str) -> str:
        """Encodes a string and returns the result.
        Parameters:
            data: String to encode.
        Returns: The encoded string result.
        """

        # empty data should return an empty string
        if not data:
            return ''

        # count + char elements held in a list before joining at the end
        encoded_elements = []

        # FSM to implement encoding
        current_char, current_count = None, 0
        for char in data:
            # count repeating characters, increment when repeating characters
            # are found and store the count + char when char stops repeating
            if current_char == None:
                # set the char to the current char if nothing has been set yet
                current_char = char
                current_count += 1
            elif current_char != char:
                # store pair and reset state if character not repeating
                # a pair will look like '3a' for a run of 3 repeating 'a' chars
                encoded_elements.append(str(current_count)+current_char)
                current_char = char
                current_count = 1
            else:
                # increment for repeats
                current_count += 1

        # store the very last pair of count + char
        encoded_elements.append(str(current_count)+current_char)

        # return a string that can be easily stored and transported
        # a space is used as a delimiter here between count + char pairs
        # i.e. '3a 3b 5c 1e'
        return ' '.join(encoded_elements)
    
    def decode_data(data:str) -> str:
        """Decodes an encoded string and returns the result.
        Parameters:
            data: Encoded data to decode.
        Returns: The decoded string result.
        """

        # empty data should return an empty string
        if not data:
            return ''
       
        # initialize empty string to build decoded string
        decoded_string = ''

        # FSM to implement decoding
        space_seen = False

        # this is the string that tracks our current count + char pair
        current_element = ''
        for char in data:
            # if a space is seen and the current char is a space,
            # then we have double spaces, this means that only the second one
            # is our delimiter and we want to use the first space as a run
            if space_seen and char != ' ':
                # a current element will look like '10a ' where
                # current_element[:-2] will be the count, '10' and
                # current_element[-2] will be the 'a' the character
                # current_element[-1] which is the delimiter which we ignore
                decoded_string += int(current_element[:-2])*current_element[-2]

                # reset space seen and set current_element to the new char
                space_seen = False
                current_element = char
            else:
                # append count + char pair to current element
                # this is used to isolate runs of characters
                current_element += char

                # note that we see a space, this is our delimiter
                if char == ' ':
                    space_seen = True

        # add the final count + char pair/element, no trailing space at end
        decoded_string += int(current_element[:-1])*current_element[-1]

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
