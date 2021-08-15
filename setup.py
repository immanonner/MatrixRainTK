from distutils.core import setup
import setuptools as setuptools

setup(
    name='matrixOnDesktop.py',
    version='1.0',
    packages=setuptools.find_packages(include=['kanji_lists']),
    requires=['kanji_lists'],
    python_requires='>=3',
    url='https://github.com/immanonner/Matrix_Code_Rain_TK/',
    license='MIT',
    author='Mothership',
    author_email='ssw.williams@gmail.com',
    description='matrixOnDesktop',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: GUI Demo',
                 'Programming Language :: Python :: 3.9'],
    keywords='Matrix Text Rain TK Tkinter GUI Demo',
    project_urls={'Source': 'https://github.com/immanonner/Matrix_Code_Rain_TK/'},
)
