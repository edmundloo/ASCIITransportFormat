from ascii_transport_format import ASCIITransportFormat
import unittest

class EncodeTest(unittest.TestCase):
    def testEncodeEmpty(self):
        """Test case for encoding an empty string.
        """
        test_case = ''
        result = ''
        self.assertEqual(ASCIITransportFormat.encode_data(test_case), result)

    def testEncode(self):
        """Test case for encoding non-empty strings.
        """
        test_cases = ['\n', ' ', 'aaabbb', 'a b', '\n\n\n', '122333']
        results = ['1\n', '1 ', '3a 3b', '1a 1  1b', '3\n', '11 22 33']
        for i in range(len(test_cases)):
            self.assertEqual(ASCIITransportFormat.encode_data(test_cases[i]), results[i])

class DecodeTest(unittest.TestCase):
    def testDecodeEmpty(self):
        """Test case for decoding an empty string.
        """
        test_case = ''
        result = ''
        self.assertEqual(ASCIITransportFormat.decode_data(test_case), result)

    def testDecode(self):
        """Test case for decoding non-empty strings.
        """
        test_cases = ['1\n', '1 ', '3a 3b', '1a 1  1b', '3\n', '11 22 33']
        results = ['\n', ' ', 'aaabbb', 'a b', '\n\n\n', '122333']
        for i in range(len(test_cases)):
            self.assertEqual(ASCIITransportFormat.decode_data(test_cases[i]), results[i])

class EncodeDecodeTest(unittest.TestCase):
    def testEncodeDecodeEmpty(self):
        """Test case for encoding and decoding an empty string.
        """
        test_case = ''
        encode_result = ASCIITransportFormat.encode_data(test_case)
        self.assertEqual(ASCIITransportFormat.decode_data(encode_result), test_case)

    def testEncodeDecode(self):
        """Test case for encoding and decoding non-empty strings.
        """
        test_cases = ['\n', ' ', 'aaabbb', 'a b', '\n\n\n', '122333']
        for i in range(len(test_cases)):
            encoded_temp = ASCIITransportFormat.encode_data(test_cases[i])
            self.assertEqual(ASCIITransportFormat.decode_data(encoded_temp), test_cases[i])

class ASCIITransportFormatTest(unittest.TestCase):
    def testEncodeDecodeEmpty(self):
        """Test case for encoding an empty string using ASCIITransportFormat object.
        """
        test_case = ''
        obj = ASCIITransportFormat('STRING', test_case)
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
        """Test case for encoding a non-pseudo encode result string using ASCIITransportFormat object.
        """
        test_case = 'aaaa1111\nbbbb2222'
        result = '4a 41 1\n 4b 42'
        obj = ASCIITransportFormat('STRING', test_case)
        self.assertEqual(obj.data, test_case)
        self.assertEqual(obj.encoded, False)
        self.assertEqual(obj.pseudo_encode, False)

        obj.encode()
        self.assertEqual(obj.data, result)
        self.assertEqual(obj.encoded, True)
        self.assertEqual(obj.pseudo_encode, False)

        obj.decode()
        self.assertEqual(obj.data, test_case)
        self.assertEqual(obj.encoded, False)
        self.assertEqual(obj.pseudo_encode, False)

    def testEncodeDecodeWithPseudo(self):
        """Test case for encoding a non-pseudo encode result string using ASCIITransportFormat object.
        """
        test_case = 'a1b2\nc3d4e5'
        obj = ASCIITransportFormat('STRING', test_case)
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

if __name__ == "__main__":
    unittest.main()
