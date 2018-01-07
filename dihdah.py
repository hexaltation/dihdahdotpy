#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test for morse code Generator/TX
# By hexaltation
# Version 0.0.3
# GPL V3
# December 2017

import sys
import os
import re
import math
import random
import argparse
import subprocess
import json
import pyaudio
import urllib.request
import wave
import time


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


def sin_wave(sample_idx, volume, frequency, sample_rate):
    return volume * math.sin(2 * math.pi * frequency * sample_idx / sample_rate)


def create_tx(durations_n_volumes, rec=False, sound=True, dest=sys.path[0]+'/',
              noise_coeff=0.0):
    if not (sound or rec):
        return -1

    frequency = 220
    sample_rate = 48000

    p = pyaudio.PyAudio()
    channels = 2

    audio_format = p.get_format_from_width(2)

    if sound:
        stream = p.open(format=audio_format, channels=channels, rate=sample_rate, output=sound)
    if rec:
        timestamp = str(time.time()).replace('.', '')
        filename = dest + timestamp + '.wav'
        file = wave.open(filename, 'wb')
        file.setnchannels(channels)
        file.setsampwidth(2)
        file.setframerate(sample_rate)

    for pair in durations_n_volumes:
        duration = pair[0]
        volume = pair[1]
        n_samples = int(sample_rate * duration)
        rest_frames = n_samples % sample_rate

        samples = []
        rest = []
        for sample_idx in range(n_samples):
            samples.append(int((sin_wave(sample_idx, volume, frequency, sample_rate) * 0x7f
                                + 0x80) * (1 - noise_coeff) +
                               (random.random() * 127 * noise_coeff)))
        for i in range(rest_frames):
            rest.append(int(0x80 * (1 - noise_coeff) + (random.random() * 127) * noise_coeff))

        if sound:
            stream.write(bytes(bytearray(samples)))
            stream.write(bytes(bytearray(rest)))
        if rec:
            file.writeframes(bytes(bytearray(samples)))
            file.writeframes(bytes(bytearray(rest)))

    if sound:
        stream.stop_stream()
        stream.close()
    p.terminate()
    if rec:
        file.close()

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


def generate_morse_msg(msg, wpm=6, rec=False, sound=True, dest=sys.path[0]+'/', noise=0.0):
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

    return create_tx(durations_n_volumes, rec, sound, dest, noise)


def generate_url(list_of_words, language):
    output = 'https://'+language+'.wikipedia.org/wiki/'
    for idx, word in enumerate(list_of_words):
        output += word.replace(' ', '_').lower()
        if len(list_of_words) > 1 and idx < (len(list_of_words)-1):
            output += '_'
    return output


def get_first_paragraph(raw_page):
    utf8_page = raw_page.decode('utf-8')
    paragraphs = re.search('<p>(.*?)</p>', utf8_page)
    first_p = paragraphs.group(0)
    clean_first_p = re.sub('<.*?>', '', first_p)
    return clean_first_p


def set_conf(config):
    conf_file_path = sys.path[0] + '/dihdah.conf'
    with open(conf_file_path, 'w') as conf_file:
        json.dump(config, conf_file)
    return 0


def get_conf():
    conf_file_path = sys.path[0] + '/dihdah.conf'
    with open(conf_file_path, 'r') as conf_file:
        config = json.load(conf_file)
    return config


def reset_conf():
    config = {'lang': 'en', 'wpm': 6, 'dest': sys.path[0] + '/', 'noise': False}
    set_conf(config)
    return config


def check_conf():
    conf_file_path = sys.path[0] + '/dihdah.conf'
    if os.path.isfile(conf_file_path):
        config = get_conf()
    else:
        config = reset_conf()
    return config


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def words_per_minute(v):
    if not v.isdigit():
        raise argparse.ArgumentTypeError('Integer value expected.')
    if int(v) < 1:
        return 1
    elif int(v) > 30:
        return 30


def string2float(v):
    try:
        float(v)
        if v < 0:
            return 0.0
        elif v > 1:
            return 1.0
    except ValueError:
        raise argparse.ArgumentTypeError('Float value expected.')


if __name__ == "__main__":
    conf = check_conf()
    parser = argparse.ArgumentParser(prog='dihdahdotpy',
                                     description='A digital Morse code operator and trainer')
    message_option = parser.add_mutually_exclusive_group()
    message_option.add_argument('-m', dest='msg', type=str, nargs='?',
                                help='the message to translate in morse code')
    message_option.add_argument('-f', dest='filename', type=str, nargs=1,
                                help='the message to translate is stored in a text file')
    message_option.add_argument('-w', dest='wiki', type=str, nargs='*',
                                help='read the definition from wikipedia.org of a given word')
    parser.add_argument('-lang', dest='lang', type=str, nargs='?',
                        help='choose the language for wikipedia.\n'
                             'Ex. for french : "fr". Default language : "en"')
    parser.add_argument('-s', dest='wpm', type=words_per_minute, nargs='?',
                        help='set speed of transmission in words per minutes. Should be an '
                             'int between 1 and 30')
    parser.add_argument('-rec', dest='rec', type=str2bool, nargs='?', default=False,
                        help='set True to save message as wave file')
    parser.add_argument('-sound', dest='sound', type=str2bool, nargs='?', default=True,
                        help='set True to Audio Stream Output')
    parser.add_argument('-d', dest='dest', type=str, nargs='?', default=False,
                        help='set destination directory of wave file')
    parser.add_argument('-n', dest='noise', type=string2float, nargs='?', default=0,
                        help='set noise coefficient. Should a float be between 0 and 1')
    config_option = parser.add_mutually_exclusive_group()
    config_option.add_argument('--save', dest='save',
                               help='save values of passed parameters in .conf file',
                               action='store_true')
    config_option.add_argument('--reset', dest='reset',
                               help='reset conf file to default values',
                               action='store_true')

    args = parser.parse_args()

    if args.lang:
        conf['lang'] = args.lang.lower()
    if args.wpm:
        conf['wpm'] = args.wpm
    if args.dest:
        conf['dest'] = args.dest
    if args.noise:
        conf['noise'] = args.noise
    if args.save:
        set_conf(conf)
    if args.reset:
        conf = reset_conf()
    if args.msg:
        generate_morse_msg(args.msg, conf['wpm'], args.rec, args.sound, conf['dest'],
                           float(conf['noise']))
    elif args.filename:
        with open(args.filename[0], 'r') as f:
            msg_from_file = f.read()
            generate_morse_msg(msg_from_file, conf['wpm'], args.rec, args.sound, conf['dest'],
                               float(conf['noise']))
    elif args.wiki:
        url = generate_url(args.wiki, conf['lang'])
        try:
            connection = subprocess.check_call(['ping', '-c', '3', '-t', '3', '8.8.8.8'],
                                               stdout=subprocess.DEVNULL,
                                               stderr=subprocess.STDOUT)
            if connection != 0:
                raise Exception('Connection to internet failed')
        except Exception as e:
            print(e)
            exit(1)
        try:
            wiki_page = urllib.request.urlopen(url).read()
            first_paragraph = get_first_paragraph(wiki_page)
            generate_morse_msg(first_paragraph, conf['wpm'], args.rec, args.sound,
                               conf['dest'], float(conf['noise']))
        except urllib.error.HTTPError:
            generate_morse_msg('HTTP Error 404: Page Not Found')
    else:
        parser.parse_args(['-h'])
