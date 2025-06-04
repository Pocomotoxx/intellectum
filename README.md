# Intellectum

This project is a Django MVP. To run the tests you will need Django installed.

First set up a virtual environment and install the dependencies. A helper
script is provided:

```bash
./scripts/setup_test_env.sh
```

If your environment does not have internet access, download the necessary
Python wheels (for example `Django`) ahead of time and place them in the
`vendor/` directory. See `vendor/README.md` for details. The setup script
will automatically use this directory when installing packages:

```bash
mkdir -p vendor
# copy Django-5.2.2-py3-none-any.whl into vendor/
./scripts/setup_test_env.sh
```

To make pip always prefer the local wheels you can use the provided
`pip.conf` which disables network access and points pip to the `vendor/`
directory:

```bash
cp pip.conf ~/.pip/pip.conf
```

After running the script, activate the environment and execute the tests:

```bash
source venv/bin/activate
cd intellektum_mvp
python manage.py test
```
