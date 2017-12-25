import os
import subprocess
import sys
import dihdah

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
        raise test
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
try:
    test = os.system("./dihdah.py -m 'test'")
    if test != 0:
        raise test
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
        raise stdout
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


if 'fail' in tests:
    print('Tests failed')
else:
    print('Tests succeed')
print('Summary:')
for idx, test in enumerate(tests):
    if test == 'success':
        print(Bcolors.OKGREEN + 'Test ' + str(idx + 1) + ' ' + test + Bcolors.ENDC)
    elif test == 'fail':
        print(Bcolors.FAIL + 'Test ' + str(idx + 1) + ' ' + test + Bcolors.ENDC)

# TODO :
# Check Save
# Check reset
# Check -w
# Check -w 404
# Check -w without argument
# Check -m without argument
# Check Noise (may be set random seed) checksum of file essence ffmpeg hash
# unitary test passing and non passing for all functions
# And many more