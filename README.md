# ASCII Transport Format

A module that allows for encoding, lossless compression, and decoding of ASCII art. The module supports object encoding (which also compresses), object decoding, object to JSON and JSON to object conversion, as well as file (containing ASCII art) to object conversion. 

## Prerequisites

The project is built in and requires Python 3.

## Usage

This module is designed to be used as a suite of tools. The tests and in-code comments describe usage of the tools. 
Some basic and incomplete usage of the tools is shown below.

After importing the module:
```
from ascii_transport_format import ASCIITransportFormat
```

Construct your object using a file or a string representing the ASCII art:
```
your_object = ASCIITransportFormat(ASCIITransportFormat.SupportedTypes.FILE, your_file_name)
```
or
```
your_object = ASCIITransportFormat(ASCIITransportFormat.SupportedTypes.STRING, your_ascii_string)
```

Encode your object:
```
your_object.encode()
```

Get your object JSON and send it over the web:
```
your_json = your_object.json()
# send your JSON somewhere
```

Reconstruct your object with the JSON representing an ASCIITransportFormat object:
```
received_object = ASCIITransportFormat(ASCIITransportFormat.SupportedTypes.JSON, received_json)
```

Decode your object:
```
received_object.decode()
```

Get the decoded data and do something with it:
```
received_data = received_object.get_data()
# display your received data
```


## Unit Tests

Run the basic encode/decode unit tests using the following command:

```
python3 test_ascii_transport_format.py 
```

### Coverage
These unit tests cover basic usage for the core processing function, `encode_data` and `decode_data`. Test cases include empty strings, and a variety of regular string test cases that include a variety of different characters. This is a very basic test essentially used as a sanity test to make sure the function's core functionality is valid. There is also coverage for the `pseudo_encode` functionality mentioned below as well as `encode` and `decode` using an ASCIITransportFormat object.

## Algorithm
The `ASCIITransportFormat` utilizes a run-length encoding data compression algorithm in order to encode and compress ASCII art to a smaller size, more suitable for transport. For example, the `data.txt` file in this folder consists of 5495 characters before compression. After encoding the ASCII art, it only takes up 3457 characters which is significantly less. This algorithm also allows for me to decode the encoded object without losing any data at all. This algorithm relies on the fact that ASCII art typically only utilizes a few characters that repeat very frequently in contiguous blocks of repetition to work optimally.

### Justification
Run-length encoding is a simple, straightforward, and effective algorithm for encoding and compressing images with many repeated values. ASCII art seems to fit within this area and I feel that this algorithm fits well in this situation. There are downsides to run-length encoding with ASCII art such as when the art doesn't contain repeated characters. If this were to happen, the encoded art would actually take up more space than un-encoded art. I overcome this problem by flagging my object as `pseudo_encode` and not actually encoding it if the encoded data is larger than the un-encoded data. This makes it so the algorithm will always produce encoded results that are equal to or smaller than the original data in size and never larger. Further improvements can be made by using more space-effective compression algorithms such as [DEFLATE](https://en.wikipedia.org/wiki/DEFLATE). In situations where every bit of space saved is desired, such as when you're hosting a ridiculous amount of images, further work for small optimizations may be worth it (such as with [Zstandard](https://code.facebook.com/posts/1658392934479273/smaller-and-faster-data-compression-with-zstandard/)), however, run-length encoding strikes a good balance between effectiveness and time needed to implement.

### Encode Data
`encode_data` runs at both O(n) space and time complexity. `encode_data` was written as a static class function so that it could be used elsewhere without creating a class instance being created. The reason is, others may have their own ways of storing encoded and decoded strings and I don't want to limit users to my object to use the algorithm. This function takes a string, encodes it, and returns it. The `encode` function actually uses the `encode_data` function and mutates it's `self` object. Encode assures that the size of the encoded data will never be larger than the size of the original data by not actually encoding (`pseudo_encode`) the data if the encoded size is larger than the original size. 

### Decode Data
`decode_data` runs at both O(n) space and time complexity. `decode_data` was also written as a static class function so it could be used elsewhere without creating a class instance, to match `encode_data`. This way, users are provided with a minimal suite to encode, compress, and decode their data while storing the data any way they want to without using my object. Decoding is actually O(1) if the string was pseudo encoded due to size issues. 

### Encoding Format
If we start with the string:
```
' aabbbccccdddddeeeeee'
```

This will encode into with a ' ' as a delimiter between multiple runs:
```
'1  2a 3b 4c 5d 6e'
```

This can then be decoded back into the original string by utilizing the description of runs that are delimited/separated by spaces.

### Tradeoffs and Improvements
- We can use a different encoding to store our numbers to reduce the amount of space large numbers take up.
- If we limit our problem size to under a certain number (i.e 100 runs max), the count in runs can be represented by a single character, with 100 runs, we can just use `chr(count)` to represent our 3 character count `100` as the single character `d`. This also enables us to more closely pack the characters since we would no longer need a delimiter (each count + char pair can be represented with two characters). I chose not to do this to make the code work for as much art as possible.
- Since ASCII art usually has many repeating characters and uses a small subset of characters, we can map each character to a value that takes up less space in memory and store these smaller values on our runs. For example, if we only use the characters `['a', 'b', 'c']`, we can map `a -> 01`, `b -> 10`, and `c -> 11`, greatly reducing the amount of stored bits.

### Benchmarks
Art | Original Size | Encoded Size | Percent Reduction
------------ | ------------- | ------------- | -------------
[startrk2.txt](http://www.textfiles.com/art/startrk2.art) | 113947 | 50612 | 55.6%
[sunlogo.txt](http://www.textfiles.com/art/sunlogo.txt) | 213 | 213 | 0%
[deborah.txt](http://www.textfiles.com/art/deborah.art) | 10582 | 9282 | 12.3%
[monalisa.txt](http://www.textfiles.com/art/monalisa.art) | 28681 | 18978 | 33.8%
[ferrari.txt](http://www.textfiles.com/art/ferrari.art) | 42688 | 20578 | 51.8%
