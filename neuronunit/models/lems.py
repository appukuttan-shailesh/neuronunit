"""Model classes for NeuronUnit"""

import os
try:
    from tempfile import TemporaryDirectory
except:
    from backports.tempfile import TemporaryDirectory
import inspect
import shutil
import random
import pickle

from lxml import etree

import sciunit
import neuronunit.capabilities as cap
from pyneuroml import pynml
from .base import RunnableModel


class LEMSModel(RunnableModel,
                cap.Runnable,
                ):
    """A generic LEMS model"""

    def __init__(self, LEMS_file_path, name=None,
                    backend=None, attrs=None):
        if name is None:
            name = os.path.split(LEMS_file_path)[1].split('.')[0]
        self.orig_lems_file_path = os.path.abspath(LEMS_file_path)
        assert os.path.isfile(self.orig_lems_file_path),\
            "'%s' is not a file" % self.orig_lems_file_path
        # Use original path unless create_lems_file is called
        self.lems_file_path = self.orig_lems_file_path
        if backend is None:
            backend = 'jNeuroML'
        super(LEMSModel,self).__init__(name, backend=backend, attrs=attrs)
        self.set_default_run_params(**pynml.DEFAULTS)
        self.set_default_run_params(nogui=True)

    def get_nml_paths(self, lems_tree=None, absolute=True, original=False):
        if not lems_tree:
            lems_tree = etree.parse(self.lems_file_path)
        nml_paths = [x.attrib['file'] for x in \
                     lems_tree.xpath("Include[contains(@file, '.nml')]")]
        if absolute: # Turn into absolute paths
            lems_file_path = self.orig_lems_file_path if original \
                                                      else self.lems_file_path
            nml_paths = [os.path.join(os.path.dirname(lems_file_path),x) \
                         for x in nml_paths]
        return nml_paths

    def create_lems_file_copy(self, name=None, use=True):
        """Creates a temporary, writable copy of the original LEMS file so that
        e.g. edits can be made to it programatically before simulation
        """
        if name is None:
            name = self.name
        if not hasattr(self,'temp_dir'):
            self.temp_dir = TemporaryDirectory()
        lems_copy_path  = os.path.join(self.temp_dir.name, '%s.xml' % name)
        shutil.copy2(self.orig_lems_file_path,lems_copy_path)
        nml_paths = self.get_nml_paths(original=True)
        for orig_nml_path in nml_paths:
            new_nml_path = os.path.join(self.temp_dir.name,
                                        os.path.basename(orig_nml_path))
            shutil.copy2(orig_nml_path,new_nml_path)
        if self.attrs:
            self.set_lems_attrs(path=lems_copy_path)
        if use:
            self.lems_file_path = lems_copy_path
        return lems_copy_path

    def set_lems_attrs(self, path=None):
        if path is None:
            path = self.lems_file_path
        paths = [path] + self.get_nml_paths()
        for p in paths:
            tree = etree.parse(p)
            for key1,value1 in self.attrs.items():
                nodes = tree.findall(key1)
                for node in nodes:
                    for key2,value2 in value1.items():
                        node.attrib[key2] = value2
            tree.write(p)

    def set_lems_run_params(self, verbose=False):
        from lxml import etree
        from neuroml import nml
        lems_tree = etree.parse(self.lems_file_path)
        trees = {self.lems_file_path:lems_tree}

        # Edit LEMS files.
        nml_paths = self.get_nml_paths(lems_tree=lems_tree)
        trees.update({x:nml.nml.parsexml_(x) for x in nml_paths})

        # Edit NML files.
        for file_path,tree in trees.items():
            for key,value in self.run_params.items():
                if key == 'injected_square_current':
                    pulse_generators = tree.findall('pulseGenerator')
                    for pg in pulse_generators:
                        for attr in ['delay', 'duration', 'amplitude']:
                            if attr in value:
                                if verbose:
                                    print('Setting %s to %f' % (attr,value[attr]))
                                pg.attrib[attr] = '%s' % value[attr]

            tree.write(file_path)