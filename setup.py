"""The setup module for the d8base-backend."""
import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()
DESC = 'The REST server for the d8base.com'

setup(
    name='d8base-backend',
    version='0.0.1',
    description=DESC,
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/maxi-booking/d8base-backend',
    author='maxi-booking',
    author_email='info@maxi-booking.com',
    license='GPL-3.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.7.0',
    packages=find_packages(
        exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    include_package_data=True,
    install_requires=[
        'Django>=3.0.0',
        'django-environ==0.4.5',
        'django-cors-headers==3.2.1',
        'django-modeltranslation==0.14.4',
        'django-admin-sortable==2.2.3',
        'djangorestframework==3.11.0',
        'drf-extensions==0.6.0',
        'djangorestframework-gis==0.15',
        'django-rest-registration==0.5.4',
        'django-extra-fields==2.0.5',
        'django-extensions==2.2.8',
        'django-debug-toolbar==2.2',
        'django-reversion==3.0.7',
        'django-filter==2.2.0',
        'django-money==1.1',
        'django-otp==0.8.1',
        'django-adminactions==1.8.1',
        'django-phonenumber-field==3.0.1',
        'django-cities @ git+https://github.com/webmalc/django-cities',
        'django-crispy-forms==1.9.0',
        'django-oauth-toolkit==1.3.2',
        'django-admin-autocomplete-filter==0.4',
        'django-imagekit==4.0.2',
        'drf-yasg==1.17.1',
        'celery==4.4.0',
        'Werkzeug==1.0.0',
        'phonenumbers==8.11.3',
        'qrcode==6.1',
        'sentry-sdk==0.14.1',
        'arrow==0.15.5',
        'redis==3.4.1',
        'psycopg2==2.8.4',
        'python-memcached==1.59',
        'Pillow==7.0.0',
        'pytz==2020.1',
    ],
)
