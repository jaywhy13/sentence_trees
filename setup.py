from setuptools import setup

setup(name='sentence_trees',
      version='0.1',
      description='Sentence trees - a package built allows trees to be built from a list of sentences to allow for auto-completion',
      url='http://github.com/jaywhy13/sentence_trees',
      author='Jean-Mark Wright',
      author_email='jeanmark.wright@gmail.com',
      license='MIT',
      packages=['sentence_trees'],
      install_requires=[
            'Django>=1.5.5,<=2.0.0',
            'node>=0.9.12',
      ],
      zip_safe=False)
