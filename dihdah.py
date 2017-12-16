# Test for morse code Generator/TX

import pyaudio
import re
import math
import argparse
from urllib.request import urlopen


def get_code():
    morse = {'a': '._',      'n': '_.',       '1': '.____',
             'b': '_...',    'o': '___',      '2': '..___',
             'c': '_._.',    'p': '.__.',     '3': '...__',
             'd': '_..',     'q': '__._',     '4': '...._',
             'e': '.',       'r': '._.',      '5': '.....',
             'f': '.._.',    's': '...',      '6': '_....',
             'g': '__.',     't': '_',        '7': '__...',
             'h': '....',    'u': '.._',      '8': '___..',
             'i': '..',      'v': '..._',     '9': '____.',
             'j': '.___',    'w': '.__',      '0': '_____',
             'k': '_._',     'x': '_.._',
             'l': '._..',    'y': '_.__',
             'm': '__',      'z': '__..',

             '?': '..__..',  '!': '_._.__',   'à': '.__._',
             '.': '._._._',  ';': '_._._.',   'ç': '_._..',
             ':': '___...',  ',': '__..__',   'è': '._.._',
             '/': '_.._.',   '+': '._._.',    'é': '.._..',
             "'": '.____.',  '-': '_...._',   'ñ': '__.__',
             '=': '_..._',   '(': '_.__.',
             ')': '_.__._',  '_': '..__._',
             '$': '..._.._', '"': '._.._.',
             '@': '.__._.',  '&': '._...',

             'STX': '_._._',
             'ETX': '..._._',
             'STOP': '_..._',
             'ERR': '........'}
    return morse


def start_tx():
    morse = get_code()
    return morse['STX'] + ' '


def end_tx():
    morse = get_code()
    return ' ' + morse['ETX']


def create_tx(durations_n_volumes):
    frequency = 220
    sample_rate = 48000

    p = pyaudio.PyAudio()
    channels = 2
    output = True

    audio_format = p.get_format_from_width(2)
    stream = p.open(format=audio_format, channels=channels, rate=sample_rate, output=output)

    for pair in durations_n_volumes:
        duration = pair[0]
        volume = pair[1]
        n_samples = int(sample_rate * duration)
        rest_frames = n_samples % sample_rate

        s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
        samples = (int(s(t) * 0x7f + 0x80) for t in range(n_samples))
        stream.write(bytes(bytearray(samples)))
        stream.write(b'\x80' * rest_frames)

    stream.stop_stream()
    stream.close()
    p.terminate()
    return 0


def clean_msg(msg, code):
    msg = msg.lower()
    msg = msg.replace('[', '(').replace(']', ')').replace('{', '(').replace('}', ')')
    clean = ''
    for letter in msg:
        if letter not in code:
            clean += ' '
        else:
            clean += letter
    re.sub('\s{2,}', ' ', clean)
    return clean


def convert_msg(msg, code):
    coded_msg = ''
    coded_msg += start_tx()

    for letter in msg:
        if letter == ' ':
            coded_msg += letter
        else:
            for sign in code[letter]:
                coded_msg += sign
            coded_msg += '*'

    coded_msg += end_tx()
    return coded_msg


def generate_morse_msg(msg, wpm=6):
    morse = get_code()

    speed = (wpm * 50)/60
    inner_space = (1/speed, 0)
    short_pulse = [(1/speed, 1), inner_space]
    long_pulse = [(3/speed, 1), inner_space]
    outer_space = (2/speed, 0)
    # letter spaces will be inner + outer (3/speed)
    # word spaces will be inner + outer + outer (5/speed)
    
    durations_n_volumes = []

    msg = clean_msg(msg, morse)
    msg = convert_msg(msg, morse)

    for sign in msg:
        if sign == ' ' or sign == '*':
            durations_n_volumes.append(outer_space)
        elif sign == '.':
            durations_n_volumes.extend(short_pulse)
        elif sign == '_':
            durations_n_volumes.extend(long_pulse)

    return create_tx(durations_n_volumes)


def generate_url(list_of_words):
    output = 'http://www.wikipedia.org/wiki/'
    for idx, word in enumerate(list_of_words):
        output += word.replace(' ', '_')
        if len(list_of_words) > 1 and idx < (len(list_of_words)-1):
            output += '_'
    return output


def get_first_paragraph(raw_page):
    utf8_page = raw_page.decode('utf-8')
    paragraphs = re.search('<p>(.*?)<\/p>', utf8_page)
    first_paragraph = paragraphs.group(0)
    clean_first_p = re.sub('<.*?>', '', first_paragraph)
    return clean_first_p

parser = argparse.ArgumentParser(prog='dihdahdotpy', description='A digital Morse code '
                                                                 'operator and trainer')
parser.add_argument('-m', dest='msg', type=str, nargs='?', help='The message to '
                                                                'translate in morse '
                                                                'code')
parser.add_argument('-f', dest='filename', type=str, nargs=1, help='The message to '
                                                                   'translate '
                                                                   'is stored in a file')
parser.add_argument('-w', dest='wiki', type=str, nargs='*', help='Read the definition from '
                                                                 'wikipedia.org of a given '
                                                                 'word')

args = parser.parse_args()
print(args)
if args.msg is not None:
    generate_morse_msg(args.msg)
elif args.filename is not None:
    with open(args.filename[0], 'r') as f:
        msg_from_file = f.read()
        generate_morse_msg(msg_from_file)
elif args.wiki is not None:
    url = generate_url(args.wiki)
    wiki_page = urlopen(url).read()
    first_paragraph = get_first_paragraph(wiki_page)
    generate_morse_msg(first_paragraph)
else:
    parser.parse_args(['-h'])
