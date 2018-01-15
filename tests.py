import os
import subprocess
import sys
import dihdah
import filecmp
import urllib
import re

tests = []


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Test 1 Check launch command without any options
print(Bcolors.OKBLUE + '_____Test 1_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Check launch command without any options' + Bcolors.ENDC)
try:
    test = os.system("./dihdah.py")
    if test != 0:
        raise Exception(test)
    else:
        print(Bcolors.OKGREEN + 'Test 1 passed\n' + Bcolors.ENDC)
        tests.append('success')
except Exception as e:
    print(e)
    print(Bcolors.FAIL + 'Failed to pass test 1\n' + Bcolors.ENDC)
    tests.append('fail')

# Test 2 Check test message emission
print(Bcolors.OKBLUE + '_____Test 2_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Tx message "test"' + Bcolors.ENDC)
if os.path.isfile(sys.path[0] + '/dihdah.conf'):
    try:
        os.remove(sys.path[0] + '/dihdah.conf')
        print('dihdah.conf removed')
    except Exception as e:
        print(e)
    finally:
        print('There is no (more) dihdah.conf in the current folder')
try:
    test = os.system("./dihdah.py -m 'test'")
    if test != 0:
        raise Exception(test)
    else:
        print(Bcolors.OKGREEN + 'Test 2 passed\n' + Bcolors.ENDC)
        tests.append('success')
except Exception as e:
    print(e)
    print(Bcolors.FAIL + 'Failed to pass test 2\n' + Bcolors.ENDC)
    tests.append('fail')

# Test 3 Check message emission without argument
print(Bcolors.OKBLUE + '_____Test 3_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Tx message without argument' + Bcolors.ENDC)
try:
    stdout = subprocess.check_output("./dihdah.py -m", shell=True).decode(encoding='UTF-8')
    print(stdout)
    if 'usage: dihdahdotpy' not in stdout:
        raise Exception(stdout)
    else:
        print(Bcolors.OKGREEN + 'Test 3 passed\n' + Bcolors.ENDC)
        tests.append('success')
except Exception as e:
    print(e)
    print(Bcolors.FAIL + 'Failed to pass test 3\n' + Bcolors.ENDC)
    tests.append('fail')

# Test 4 conf file creation
print(Bcolors.OKBLUE + '_____Test 4_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Conf file creation' + Bcolors.ENDC)
if os.path.isfile(sys.path[0] + '/dihdah.conf'):
    try:
        os.remove(sys.path[0] + '/dihdah.conf')
        print('dihdah.conf removed')
    except Exception as e:
        print(e)
    finally:
        print('There is no (more) dihdah.conf in the current folder')
try:
    config_test = {'here': 'is', 'a': 'test'}
    if dihdah.set_conf(config_test) != 0:
        raise Exception('Config file creation failed')
    else:
        print(Bcolors.OKGREEN + 'Test 4 passed\n' + Bcolors.ENDC)
        tests.append('success')
except Exception as e:
    print(e)
    print(Bcolors.FAIL + 'Failed to pass test 4\n' + Bcolors.ENDC)
    tests.append('fail')

# Test 5 conf file reading
print(Bcolors.OKBLUE + '_____Test 5_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Conf file reading' + Bcolors.ENDC)
if os.path.isfile(sys.path[0] + '/dihdah.conf'):
    try:
        config = dihdah.get_conf()
        if config == {'here': 'is', 'a': 'test'}:
            print(Bcolors.OKGREEN + 'Test 5 passed\n' + Bcolors.ENDC)
            tests.append('success')
        else:
            raise Exception('Config file reading failed')
    except Exception as e:
        print(e)
        print(Bcolors.FAIL + 'Failed to pass test 5\n' + Bcolors.ENDC)
        tests.append('fail')
else:
    print('No conf file to check')
    print(Bcolors.FAIL + 'Failed to pass test 5\n' + Bcolors.ENDC)
    tests.append('fail')

# Test 6 save given parameters in conf file
print(Bcolors.OKBLUE + '_____Test 6_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Save given parameters in conf file' + Bcolors.ENDC)
if os.path.isfile(sys.path[0] + '/dihdah.conf'):
    try:
        os.remove(sys.path[0] + '/dihdah.conf')
        print('dihdah.conf removed')
    except Exception as e:
        print(e)
    finally:
        print('There is no (more) dihdah.conf in the current folder')
try:
    test = os.system("./dihdah.py -lang 'py' -s 9000 -d '/folda' -n 0.2 --save")
    config = dihdah.get_conf()
    if test != 0:
        raise Exception(test)
    else:
        if os.path.isfile(sys.path[0] + '/dihdah.conf'):
            try:
                config = dihdah.get_conf()
                if config['lang'] == 'py' and config['wpm'] == 30 and config['dest'] == \
                        '/folda' and config['noise'] == 0.2 and len(config) == 4:
                    print(Bcolors.OKGREEN + 'Test 6 passed\n' + Bcolors.ENDC)
                    tests.append('success')
                else:
                    raise Exception('Config file is not as expected')
            except Exception as e:
                print(e)
                print(Bcolors.FAIL + 'Failed to pass test 6\n' + Bcolors.ENDC)
                tests.append('fail')
except Exception as e:
    print(e)
    print(Bcolors.FAIL + 'Failed to pass test 6\n' + Bcolors.ENDC)
    tests.append('fail')

# Test 7 reset conf file
print(Bcolors.OKBLUE + '_____Test 7_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Reset conf file' + Bcolors.ENDC)
try:
    if os.path.isfile(sys.path[0] + '/dihdah.conf'):
        test = os.system("./dihdah.py -lang 'py' -s 9000 -d '/folda' -n 0 --reset")
        config = dihdah.get_conf()
        if test != 0:
            raise Exception(test)
        else:
            if os.path.isfile(sys.path[0] + '/dihdah.conf'):
                try:
                    config = dihdah.get_conf()
                    if config['lang'] == 'en'\
                            and config['wpm'] == 6\
                            and config['dest'] == sys.path[0] + '/'\
                            and config['noise'] == 0\
                            and len(config) == 4:
                        print(Bcolors.OKGREEN + 'Test 7 passed\n' + Bcolors.ENDC)
                        tests.append('success')
                    else:
                        raise Exception('Config file is not as expected')
                except Exception as e:
                    print(e)
                    print(Bcolors.FAIL + 'Failed to pass test 7\n' + Bcolors.ENDC)
                    tests.append('fail')
    else:
        raise Exception('No config file to reset')
except Exception as e:
    print(e)
    print(Bcolors.FAIL + 'Failed to pass test 7\n' + Bcolors.ENDC)
    tests.append('fail')

# Test 8 Check message emission from file without argument
print(Bcolors.OKBLUE + '_____Test 8_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Tx message without argument in -f mode' + Bcolors.ENDC)
output = ''
try:
    stdout = subprocess.check_output("./dihdah.py -f", shell=True).decode(encoding='UTF-8')
except subprocess.CalledProcessError as e:
    output = e.returncode
try:
    if output == 0:
        raise Exception('Call of -f without argument must have failed')
    else:
        print(Bcolors.OKGREEN + 'Test 8 passed\n' + Bcolors.ENDC)
        tests.append('success')
except Exception as e:
    print(e)
    print(Bcolors.FAIL + 'Failed to pass test 8\n' + Bcolors.ENDC)
    tests.append('fail')

# Test 9 Check message emission from wiki without argument
print(Bcolors.OKBLUE + '_____Test 9_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Tx message without argument in -w mode' + Bcolors.ENDC)
try:
    stdout = subprocess.check_output("./dihdah.py -w", shell=True).decode(encoding='UTF-8').rstrip()
    print(stdout)
    if 'usage: dihdahdotpy' not in stdout:
        raise Exception(stdout)
    else:
        print(Bcolors.OKGREEN + 'Test 9 passed\n' + Bcolors.ENDC)
        tests.append('success')
except Exception as e:
    print(e)
    print(Bcolors.FAIL + 'Failed to pass test 9\n' + Bcolors.ENDC)
    tests.append('fail')

# Test 10 Check test message emission from file
print(Bcolors.OKBLUE + '_____Test 10_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Tx message "HTTP Error 404: Page Not Found" in -f mode' + Bcolors.ENDC)
if os.path.isfile(sys.path[0] + '/dihdah.conf'):
    try:
        os.remove(sys.path[0] + '/dihdah.conf')
        print('dihdah.conf removed')
    except Exception as e:
        print(e)
    finally:
        print('There is no (more) dihdah.conf in the current folder')
try:
    sourcefile = sys.path[0] + '/test.txt'
    os.system("echo 'HTTP Error 404: Page Not Found' > test.txt")
    test = os.system("./dihdah.py -f '" + sourcefile + "' -o modeFileTest -rec 1")
    if os.path.isfile(sys.path[0] + '/test.txt'):
        try:
            os.remove(sys.path[0] + '/test.txt')
            print('test.txt removed')
        except Exception as e:
            print(e)
        finally:
            print('There is no (more) test.txt in the current folder')
    if test != 0:
        raise Exception(test)
    else:
        print(Bcolors.OKGREEN + 'Test 10 passed\n' + Bcolors.ENDC)
        tests.append('success')
except Exception as e:
    print(e)
    print(Bcolors.FAIL + 'Failed to pass test 10\n' + Bcolors.ENDC)
    tests.append('fail')

# Test 11 Check -w mode 404 error
print(Bcolors.OKBLUE + '_____Test 11_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Check mode -w 404 error' + Bcolors.ENDC)
try:
    test = os.system("./dihdah.py -w 'dihdahdotpy' -o wiki404Test -rec 1")
    if test != 0:
        raise Exception(test)
    elif filecmp.cmp(sys.path[0] + '/modeFileTest.wav', sys.path[0] + '/wiki404Test.wav'):
        try:
            os.remove(sys.path[0] + '/modeFileTest.wav')
            print('modeFileTest removed')
        except Exception as e:
            print(e)
        finally:
            print('There is no (more) modeFileTest.wav in the current folder')
        print(Bcolors.OKGREEN + 'Test 11 passed\n' + Bcolors.ENDC)
        tests.append('success')
    else:
        raise Exception('The two files are different')
except Exception as e:
    print(e)
    print(Bcolors.FAIL + 'Failed to pass test 11\n' + Bcolors.ENDC)
    tests.append('fail')

# Test 12 Check -w mode
print(Bcolors.OKBLUE + '_____Test 12_____' + Bcolors.ENDC)
print(Bcolors.HEADER + 'Check -w mode' + Bcolors.ENDC)
try:
    try:
        connection = subprocess.check_call(['ping', '-c', '3', '-t', '3', '8.8.8.8'],
                                           stdout=subprocess.DEVNULL,
                                           stderr=subprocess.STDOUT)
        if connection != 0:
            raise Exception('Connection to internet failed')
    except Exception as e:
        print(e)
    short_w = urllib.request.urlopen('https://en.wikipedia.org/wiki/Special:ShortPages').read()
    utf8_w = short_w.decode('utf-8')
    lis = re.search('<li>(.*?)</li>', utf8_w)
    first_li = lis.group(0)
    clean_first_li = re.sub('>.*?</a>', '', first_li)
    clean_address = clean_first_li.split('"')[3]
    test = os.system("./dihdah.py -w '" + str(clean_address) + "' -o wiki -rec 1")
    if test != 0:
        raise Exception(test)
    elif not filecmp.cmp(sys.path[0] + '/wiki.wav', sys.path[0] + '/wiki404Test.wav'):
        try:
            os.remove(sys.path[0] + '/wiki404Test.wav')
            print('wiki404Test.wav removed')
            os.remove(sys.path[0] + '/wiki.wav')
            print('wiki.wav removed')
        except Exception as e:
            print(e)
        finally:
            print('There is no (more) wiki404Test.wav nor wiki.wav in the current folder')
        print(Bcolors.OKGREEN + 'Test 12 passed\n' + Bcolors.ENDC)
        tests.append('success')
    else:
        raise Exception('The two files are equal')
except Exception as e:
    print(e)
    print(Bcolors.FAIL + 'Failed to pass test 12\n' + Bcolors.ENDC)
    tests.append('fail')


# Tests Summary
if 'fail' in tests:
    print(Bcolors.FAIL + '\nTests failed\n' + Bcolors.ENDC)
else:
    print(Bcolors.OKGREEN + '\nTests Succeed\n' + Bcolors.ENDC)
print('Summary:')
for idx, test in enumerate(tests):
    if test == 'success':
        print(Bcolors.OKGREEN + 'Test ' + str(idx + 1) + ' ' + test + Bcolors.ENDC)
    elif test == 'fail':
        print(Bcolors.FAIL + 'Test ' + str(idx + 1) + ' ' + test + Bcolors.ENDC)


# TODO :
# Check Noise (may be set random seed) checksum of file essence ffmpeg hash
# unitary test passing and non passing for all functions
# Check mutual exclusions
# Isolate test as function in order to be called as subset of tests from testing library
# rewrite tests with tries around
# Suppress All test files after tests are done.
# Make a function and push file names in a list when they're created
# And many more
