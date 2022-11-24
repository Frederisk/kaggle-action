# kaggle action

Execute CI/CD with [kaggle](https://www.kaggle.com/). You can use the free kaggle GPU resource to complete the test. This Action is inspired by [lvyufeng/action-kaggle-gpu-test](https://github.com/lvyufeng/action-kaggle-gpu-test) and [namiyousef/action-kaggle-gpu-test](https://github.com/namiyousef/action-kaggle-gpu-test).

## Feature

Kaggle provides a series of remote control tools and free GPU resources. And these resources can be used in CI/CD after combination.

For free users, kaggle will provide more than 30 hours of GPU usage per week, which is enough to provide enough testing for some small projects. For some open source projects, using free resources instead of renting GPU VMs yourself can save a lot of money.

## Usage

- Before using this Action, you need a [kaggle account](https://www.kaggle.com/account/login?phase=startRegisterTab).

  > In order to avoid abuse of server resources, kaggle may require you to use your mobile phone number for verification. If your network is unavailable or the GPU is unavailable during execution, it may be that kaggle restricts the use of unauthenticated users.

- Then go to your account page. Create your API Token. You'll get a file with something like this:

  ```json
  {
    "username": "USERNAME",
    "key": "TOKEN"
  }
  ```

- Add `USERNAME` and `TOKEN` to the secret of your GitHub repository respectively.
- Then create your workflows file, for example:

  ```yaml
  name: kaggle gpu test
  on:
    push: [master, main]
  jobs:
    kaggle-ci:
      name: kaggle CI
      runs-on: ubuntu-latest
      steps:
        - name: Checkout repository
          uses: actions/checkout@v3
        - name: Run kaggle
          uses: Frederisk/kaggle-action@v1.0.0
          with:
            username: ${{ secrets.KAGGLE_USERNAME }}
            key: ${{ secrets.KAGGLE_TOKEN }}
            # The name of the kaggle used for testing, take a new one.
            # Try to avoid underscores, spaces or other special characters.
            title: KaggleTestCI
            # The location of your test script, which we will write next.
            code_file: .github/script/gpu_runner.py
  ```

- Finally, you can write your own script to test. In particular, the script will be executed on Kaggle's server, not GitHub Action's server, so you may also need to clone the repository to the server. In a python script, you can execute external commands through functions such as `os.system`, `subprocess.call`, `subprocess.run`, etc. Here's a simple example:

  ```python
  import os
  import subprocess

  def callsh(command):
    status = subprocess.run(command)
    status.check_returncode()
    print(status.stdout)

  callsh(['git', 'clone', 'https://github.com/name/repo_name'])
  os.chdir('repo_name')
  callsh(['bash', 'scripts/setup.sh'])
  callsh(['conda', 'create', '-n', 'testenv', 'python=3.8.12', 'cudatoolkit=9.2', 'cudnn', '-y'])
  callsh(['/opt/conda/envs/testenv/bin/pip', 'install', '-r', 'requirements.txt'])
  callsh(['/opt/conda/envs/testenv/bin/pytest', 'tests'])
  # ......
  ```

## Parameters

These parameters are slightly different from the kaggle api, but [the kaggle api's docs](https://github.com/Kaggle/kaggle-api/wiki/Kernel-Metadata) may still be informative.

- `username`: Required. Your kaggle username.
- `key`: Required. Your kaggle key/token.
- `title`: Required. The title of the kernel. Please be aware that kernel titles and slugs are linked to each other. A kernel slug is always the title lowercased with dashes (`-`) Replacing spaces.
- `code_file`: Required. The path to your kernel source code.
- `language`: Default value is `python`. The language your kernel is written in. Valid options are `python`, `r`, and `rmarkdown`.
- `kernel_type`: Default value is `script`. The type of kernel. Valid options are `script` and `notebook`.
- `enable_gpu`: Default value is `enable`. Whether or not the kernel should run on a GPU. `enable` to run on the GPU, otherwise not.
- `enable_internet`: Default value is `enable`. Whether or not the kernel should be able to access the internet. `enable` to use the internet, otherwise not.

## Known Issues

- When the `title` has an underscore, the status of the execution instance may not be obtained.
- The kaggle's server is not a real virtual machine, it is actually executed in docker. So some system commands or programs cannot work properly. For example, trying to start docker (`service docker start`) will get an error: `cannot create directory "cpuset"`.
