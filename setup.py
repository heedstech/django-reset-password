import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-reset-password',
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    description='Django password reset with code.',
    long_description=README,
    author='Willian Abdon',
    author_email='willian.abdom@gmail.com',
    url='https://github.com/heedstech/django-reset-password',
    license='MIT',
    python_requires=">=3.7",
    install_requires=[
        'django',
        'djangorestframework'
    ],
)