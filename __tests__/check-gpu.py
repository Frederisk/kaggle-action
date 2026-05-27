import sys
import subprocess

EXPECTED_SHAPE = "___EXPECTED_SHAPE___"

def check_gpu():
    try:
        output = subprocess.check_output(['nvidia-smi', '-L'], stderr=subprocess.STDOUT).decode('utf-8').strip()

        print(f'GPU detected: {output}')

        if EXPECTED_SHAPE == 'NvidiaTeslaP100' and 'P100' not in output:
            print('Check failed: Expected Nvidia Tesla P100 GPU, but not found.')
            sys.exit(1)
        if EXPECTED_SHAPE == 'NvidiaTeslaT4' and 'T4' not in output:
            print('Check failed: Expected Nvidia Tesla T4 GPU, but not found.')
            sys.exit(1)
        if EXPECTED_SHAPE == "":
            print('Check failed: No expected machine shape specified, but GPU detected.')
            sys.exit(1)

        print('GPU check passed.')
        sys.exit(0)
    except FileNotFoundError:
        if EXPECTED_SHAPE == "":
            print('Check successful: No GPU detected as expected.')
            sys.exit(0)
        else:
            print('Check failed: Expected GPU not detected, and nvidia-smi command not found.')
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        if EXPECTED_SHAPE == "":
            print('Check successful: No GPU detected as expected.')
            sys.exit(0)
        else:
            print(f'Check failed: Expected GPU not detected. nvidia-smi output: {e.output.decode("utf-8")}')
            sys.exit(1)

if __name__ == '__main__':
    check_gpu()
