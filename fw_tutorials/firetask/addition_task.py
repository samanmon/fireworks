#!/usr/bin/env python

"""
TODO: add docs
"""
from fireworks.core.firetask import FireTaskBase
from fireworks.utilities.fw_serializers import FWSerializable
from fireworks.core.firework import FireWork, FWAction

__author__ = 'Anubhav Jain'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Anubhav Jain'
__email__ = 'ajain@lbl.gov'
__date__ = 'Feb 17, 2013'


class AdderTask(FireTaskBase, FWSerializable):
    
    _fw_name = "Addition Task"
    
    def run_task(self, fw):
        input_array = fw.spec['input_array']
        m_sum = sum(input_array)

        with open('sum_output.txt', 'w') as f:
            f.write("The sum of {} is: {}".format(input_array, m_sum))

        return FWAction('CONTINUE', {'sum': m_sum})
        
if __name__ == '__main__':
    fw = FireWork(AdderTask({}), {"input_array": [1, 2]})
    fw.to_file("fw_adder.yaml")