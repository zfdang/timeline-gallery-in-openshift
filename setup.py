from setuptools import setup

setup(name='www.zfdang.com',
      version='1.0',
      description='timeline gallery in openshift',
      author='Zhengfa DANG',
      author_email='dantifer@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      # install_requires=['Django>=1.3'],
      # http://pypi.python.org/pypi
      install_requires=['flask', 'sqlalchemy', 'flask-babel', 'simple-pbkdf2', 'PIL'],
)
