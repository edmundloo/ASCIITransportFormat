import unittest
from ascii_transport_format import ASCIITransportFormat


class EncodeTest(unittest.TestCase):
    def testEncodeEmpty(self):
        """Test case for encoding an empty string.
        """
        empty_case = ''
        encoded_result = ASCIITransportFormat.encode_data(empty_case)
        self.assertEqual(encoded_result, empty_case)

    def testEncode(self):
        """Test case for encoding non-empty strings.
        """
        test_cases = [
            ('\n', '1\n'),
            (' ', '1 '),
            ('aaabbb', '3a 3b'),
            ('a b', '1a 1  1b'),
            ('\n\n\n', '3\n'),
            ('122333', '11 22 33'),
            ('aaaaaaaaaa', '10a'),
            ('aaaaaaaaaabbbbbbbbbbb', '10a 11b'),
            ('a'*1001, '1001a'),
            (''.join(['a'*1001, 'b'*909, 'c'*65, 'd'*2]), '1001a 909b 65c 2d'),
        ]
        for data, expected in test_cases:
            encoded_result = ASCIITransportFormat.encode_data(data)
            self.assertEqual(encoded_result, expected)


class DecodeTest(unittest.TestCase):
    def testDecodeEmpty(self):
        """Test case for decoding an empty string.
        """
        empty_case = ''
        decoded_result = ASCIITransportFormat.decode_data(empty_case)
        self.assertEqual(decoded_result, empty_case)

    def testDecode(self):
        """Test case for decoding non-empty strings.
        """
        test_cases = [
            ('1\n', '\n'),
            ('1 ', ' '),
            ('3a 3b', 'aaabbb'),
            ('1a 1  1b', 'a b'),
            ('3\n', '\n\n\n'),
            ('11 22 33', '122333'),
            ('10a', 'aaaaaaaaaa'),
            ('10a 11b', 'aaaaaaaaaabbbbbbbbbbb'),
            ('1001a', 'a'*1001),
            ('1001a 909b 65c 2d', ''.join(['a'*1001, 'b'*909, 'c'*65, 'd'*2])),
        ]
        for data, expected in test_cases:
            decoded_result = ASCIITransportFormat.decode_data(data)
            self.assertEqual(decoded_result, expected)


class EncodeDecodeTest(unittest.TestCase):
    def testEncodeDecodeEmpty(self):
        """Test case for encoding and decoding an empty string.
        """
        empty_case = ''
        encoded_result = ASCIITransportFormat.encode_data(empty_case)
        decoded_result = ASCIITransportFormat.decode_data(encoded_result)
        self.assertEqual(decoded_result, empty_case)

    def testEncodeDecode(self):
        """Test case for encoding and decoding non-empty strings.
        """
        test_cases = [
            '\n',
            ' ',
            'aaabbb',
            'a b',
            '\n\n\n',
            '122333',
            'aaaaaaaaaa',
            'aaaaaaaaaabbbbbbbbbbb',
            'a'*1001,
            ''.join(['a'*1001, 'b'*909, 'c'*65, 'd'*2]),
        ]
        for data in test_cases:
            encoded_result = ASCIITransportFormat.encode_data(data)
            decoded_result = ASCIITransportFormat.decode_data(encoded_result)
            self.assertEqual(decoded_result, data)


class ASCIITransportFormatStringTest(unittest.TestCase):
    def testEncodeDecodeEmpty(self):
        """
        Test case for encoding an empty string
        using ASCIITransportFormat STRING object.
        """
        test_case = ''
        obj = ASCIITransportFormat(
            ASCIITransportFormat.SupportedTypes.STRING,
            test_case,
        )
        self.assertEqual(obj.data, test_case)
        self.assertEqual(obj.encoded, False)
        self.assertEqual(obj.pseudo_encode, False)

        obj.encode()
        self.assertEqual(obj.data, test_case)
        self.assertEqual(obj.encoded, True)
        self.assertEqual(obj.pseudo_encode, True)

        obj.decode()
        self.assertEqual(obj.data, test_case)
        self.assertEqual(obj.encoded, False)
        self.assertEqual(obj.pseudo_encode, False)

    def testEncodeDecodeNonPseudo(self):
        """
        Test case for encoding a non-pseudo encode result
        string using ASCIITransportFormat STRING object.
        """
        test_cases = [
            ('aaabbb', '3a 3b'),
            ('\n\n\n', '3\n'),
            ('aaaaaaaaaa', '10a'),
            ('aaaaaaaaaabbbbbbbbbbb', '10a 11b'),
            ('a'*1001, '1001a'),
            (''.join(['a'*1001, 'b'*909, 'c'*65, 'd'*2]), '1001a 909b 65c 2d'),
            ('aaaa1111\nbbbb2222', '4a 41 1\n 4b 42'),
        ]
        for data, expected in test_cases:
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.STRING,
                data,
            )
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

            obj.encode()
            self.assertEqual(obj.data, expected)
            self.assertEqual(obj.encoded, True)
            self.assertEqual(obj.pseudo_encode, False)

            obj.decode()
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

    def testEncodeDecodeWithPseudo(self):
        """
        Test case for encoding a non-pseudo encode result
        string using ASCIITransportFormat STRING object.
        """
        test_cases = [
            '\n',
            ' ',
            'a b',
            '122333',
            'a1b2\nc3d4e5',
        ]
        for data in test_cases:
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.STRING,
                data,
            )
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

            obj.encode()
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, True)
            self.assertEqual(obj.pseudo_encode, True)

            obj.decode()
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)


class ASCIITransportFormatJSONTest(unittest.TestCase):
    def testEncodeDecodeEmpty(self):
        """
        Test case for encoding an empty string
        using ASCIITransportFormat JSON object.
        """
        test_case = ''
        string_obj = ASCIITransportFormat(
            ASCIITransportFormat.SupportedTypes.STRING,
            test_case,
        )
        json_obj = string_obj.json()
        obj = ASCIITransportFormat(
            ASCIITransportFormat.SupportedTypes.JSON,
            json_obj,
        )
        self.assertEqual(obj.data, test_case)
        self.assertEqual(obj.encoded, False)
        self.assertEqual(obj.pseudo_encode, False)

        json_obj = obj.json()
        obj = ASCIITransportFormat(
            ASCIITransportFormat.SupportedTypes.JSON,
            json_obj,
        )
        obj.encode()
        self.assertEqual(obj.data, test_case)
        self.assertEqual(obj.encoded, True)
        self.assertEqual(obj.pseudo_encode, True)

        json_obj = obj.json()
        obj = ASCIITransportFormat(
            ASCIITransportFormat.SupportedTypes.JSON,
            json_obj,
        )
        obj.decode()
        self.assertEqual(obj.data, test_case)
        self.assertEqual(obj.encoded, False)
        self.assertEqual(obj.pseudo_encode, False)

    def testEncodeDecodeNonPseudo(self):
        """
        Test case for encoding a non-pseudo encode result
        string using ASCIITransportFormat JSON object.
        """
        test_cases = [
            ('aaabbb', '3a 3b'),
            ('\n\n\n', '3\n'),
            ('aaaaaaaaaa', '10a'),
            ('aaaaaaaaaabbbbbbbbbbb', '10a 11b'),
            ('a'*1001, '1001a'),
            (''.join(['a'*1001, 'b'*909, 'c'*65, 'd'*2]), '1001a 909b 65c 2d'),
            ('aaaa1111\nbbbb2222', '4a 41 1\n 4b 42'),
        ]
        for data, expected in test_cases:
            string_obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.STRING,
                data
            )
            json_obj = string_obj.json()
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.JSON,
                json_obj,
            )
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

            json_obj = obj.json()
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.JSON,
                json_obj,
            )
            obj.encode()
            self.assertEqual(obj.data, expected)
            self.assertEqual(obj.encoded, True)
            self.assertEqual(obj.pseudo_encode, False)

            json_obj = obj.json()
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.JSON,
                json_obj,
            )
            obj.decode()
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

    def testEncodeDecodeWithPseudo(self):
        """
        Test case for encoding a non-pseudo encode result
        string using ASCIITransportFormat JSON object.
        """
        test_cases = [
            '\n',
            ' ',
            'a b',
            '122333',
            'a1b2\nc3d4e5',
        ]
        for data in test_cases:
            string_obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.STRING,
                data,
            )
            json_obj = string_obj.json()
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.JSON,
                json_obj
            )
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

            json_obj = obj.json()
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.JSON,
                json_obj,
            )
            obj.encode()
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, True)
            self.assertEqual(obj.pseudo_encode, True)

            json_obj = obj.json()
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.JSON,
                json_obj,
            )
            obj.decode()
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)


class ASCIITransportFormatFileTest(unittest.TestCase):
    def testEncodeDecodeNonPseudo(self):
        """
        Test case for encoding a non-pseudo encode result
        string using ASCIITransportFormat FILE object.
        """
        test_cases = [
            ('test_files/non_pseudo_1.txt', 'aaabbb', '3a 3b'),
            ('test_files/non_pseudo_2.txt', '\n\n\n', '3\n'),
            ('test_files/non_pseudo_3.txt', 'aaaaaaaaaa', '10a'),
            (
                'test_files/non_pseudo_4.txt',
                'aaaaaaaaaabbbbbbbbbbb',
                '10a 11b'
            ),
        ]
        for data, file_data, expected in test_cases:
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.FILE,
                data,
            )
            self.assertEqual(obj.data, file_data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

            obj.encode()
            self.assertEqual(obj.data, expected)
            self.assertEqual(obj.encoded, True)
            self.assertEqual(obj.pseudo_encode, False)

            obj.decode()
            self.assertEqual(obj.data, file_data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

    def testEncodeDecodeWithPseudo(self):
        """
        Test case for encoding a non-pseudo encode result
        string using ASCIITransportFormat JSON object.
        """
        test_cases = [
            ('test_files/pseudo_1.txt', '\n'),
            ('test_files/pseudo_2.txt', ' '),
            ('test_files/pseudo_3.txt', 'a b'),
            ('test_files/pseudo_4.txt', '122333'),
        ]
        for data, file_data in test_cases:
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.FILE,
                data,
            )
            self.assertEqual(obj.data, file_data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

            obj.encode()
            self.assertEqual(obj.data, file_data)
            self.assertEqual(obj.encoded, True)
            self.assertEqual(obj.pseudo_encode, True)

            obj.decode()
            self.assertEqual(obj.data, file_data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

    def testEncodeDecodeNonPseudoSampleFiles(self):
        """
        Test case for encoding a non-pseudo encode result
        string using ASCIITransportFormat FILE object. This function
        specifically uses the sample ASCII art files.
        """
        test_cases = [
            'test_files/startrk2.txt',
            'test_files/ferrari.txt',
        ]
        for data in test_cases:
            file_data = None
            with open(data) as f:
                file_data = f.read()
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.FILE,
                data,
            )
            self.assertEqual(obj.data, file_data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

            obj.encode()
            self.assertEqual(obj.encoded, True)
            self.assertEqual(obj.pseudo_encode, False)

            obj.decode()
            self.assertEqual(obj.data, file_data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)


class ConstructorExceptionTest(unittest.TestCase):
    def testConstructorValueError(self):
        """
        Test case for attempting to construct an object with a bad
        data_type.
        """
        test_cases = [
            'these',
            'are',
            'bad',
            'data',
            'types',
            'FILE',
            'STRING',
            'JSON',
        ]
        for bad_data_type in test_cases:
            with self.assertRaises(ValueError):
                ASCIITransportFormat(bad_data_type, '')


class ForceEncodeTest(unittest.TestCase):
    def testNoForceEncodeValueError(self):
        """
        Test case for attempting to encode an already encoded object without
        the force flag.
        """
        test_cases = [
            ('aaabbb', '3a 3b'),
            ('\n\n\n', '3\n'),
            ('aaaaaaaaaa', '10a'),
            ('aaaaaaaaaabbbbbbbbbbb', '10a 11b'),
            ('a'*1001, '1001a'),
            (''.join(['a'*1001, 'b'*909, 'c'*65, 'd'*2]), '1001a 909b 65c 2d'),
            ('aaaa1111\nbbbb2222', '4a 41 1\n 4b 42'),
        ]
        for data, expected in test_cases:
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.STRING,
                data,
            )
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

            obj.encode()
            self.assertEqual(obj.data, expected)
            self.assertEqual(obj.encoded, True)
            self.assertEqual(obj.pseudo_encode, False)

            with self.assertRaises(ValueError):
                obj.encode()

            self.assertEqual(obj.data, expected)
            self.assertEqual(obj.encoded, True)
            self.assertEqual(obj.pseudo_encode, False)

    def testForceEncodeValueError(self):
        """
        Test case for attempting to encode an already encoded object with
        the force flag.
        """
        test_cases = [
            ('aaabbb', '3a 3b'),
            ('\n\n\n', '3\n'),
            ('aaaaaaaaaa', '10a'),
            ('aaaaaaaaaabbbbbbbbbbb', '10a 11b'),
            ('a'*1001, '1001a'),
            (''.join(['a'*1001, 'b'*909, 'c'*65, 'd'*2]), '1001a 909b 65c 2d'),
            ('aaaa1111\nbbbb2222', '4a 41 1\n 4b 42'),
        ]
        for data, expected in test_cases:
            obj = ASCIITransportFormat(
                ASCIITransportFormat.SupportedTypes.STRING,
                data,
            )
            self.assertEqual(obj.data, data)
            self.assertEqual(obj.encoded, False)
            self.assertEqual(obj.pseudo_encode, False)

            obj.encode()
            self.assertEqual(obj.data, expected)
            self.assertEqual(obj.encoded, True)
            self.assertEqual(obj.pseudo_encode, False)

            obj.encode(True)
            self.assertEqual(obj.data, expected)
            self.assertEqual(obj.encoded, True)
            self.assertEqual(obj.pseudo_encode, True)

if __name__ == "__main__":
    unittest.main()
