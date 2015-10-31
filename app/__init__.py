# coding: utf-8
"""
The MIT License (MIT)

Copyright (c) 2013 Fatih Karatana

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@package 
@date 19/06/14
@author fatih
@version 1.0.0
"""
from __future__ import division
import os
import sys
import operator
import traceback
import re

__author__ = 'fatih'
__date__ = '19/06/14'
__version__ = ''


# Set parent directory to import required files, packages or objects
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, '%s' % PARENT_DIR)

# Import Utilities class to use required helper and utility methods
from helper.Utilities import Utilities


class Statistics(object):
    """
    Statistics loads the the data contained in “HostState.txt” and "InstanceState.txt" then computes and writes out
    the summary statistics to the output file “Statistics.txt”
    """

    def __init__(self):
        """
        Constructor of Statistics class
        @return instance
        """
        super(Statistics, self).__init__()
        self.utilities = Utilities()

        # They will be set by loading conf when instance is created no need to be static
        self.host_file = None
        self.instance_file = None
        self.target_file = None

        # Load initially self files
        self.load_config()

    def fill_data_centers(self, hosts_file):
        """
        Retrieve data from configured hosts file and create a data structure to grab data centers
        @return void
        @param hosts_file source file to provide host list
        """
        data_centers = {}
        try:
            # First retrieve host list from the source file
            with open(hosts_file, "r") as h_file:
                # Gather content of file and split lines
                content = h_file.read()

                # Check file content
                if self.check_file(content):
                    content = content.splitlines()
                    for line in content:
                        new_line = line.split(",")
                        if new_line[2] in data_centers:
                            data_centers[new_line[2]][new_line[0]] = {
                                "number_of_slots": new_line[1],
                                "instances": []
                            }
                        else:
                            data_centers[new_line[2]] = {
                                new_line[0]: {
                                    "number_of_slots": new_line[1],
                                    "instances": []
                                }
                            }
                        # Fill the object with instances
                        self.write_instances(
                            key=new_line[0],
                            target=data_centers[new_line[2]][new_line[0]])
                    return data_centers
                else:
                    raise SyntaxError("Content loaded from host file is malformed.")

        except EOFError as err:
            Utilities.log(Utilities.logging.ERROR, err)
        except IOError:
            Utilities.log(Utilities.logging.ERROR, "There is no required file to retrieve hosts in given path.")
        except SyntaxError as err:
            Utilities.log(Utilities.logging.ERROR, err)
        except IndexError:
            Utilities.log(Utilities.logging.CRITICAL, "Content of file is malformed")

    def write_instances(self, target=None, key=None):
        """
        This method write instances retrieved from class instances file and push those instances into given target
        @param target a data structure preferably dictionary
        @return void
        """
        try:
            # Fill the object with instances
            with open(self.instance_file, "r") as h_file:
                # Gather content of file and split lines
                content = h_file.read()

                # Check file content
                if self.check_file(content):
                    content = content.splitlines()
                    for line in content:
                        new_line = line.split(",")
                        # Set instances into the host which, they belong to
                        if new_line[2] == key:
                            target["instances"].append({
                                "instance_id": new_line[0],
                                "customer_id": new_line[1]
                            })
                            # It is a class instance's object but it mostly will be required in some other cases
                            # that is why it is better to also return the class object
                else:
                    raise SyntaxError("Content loaded from instance file is malformed.")
        except EOFError as err:
            Utilities.log(Utilities.logging.ERROR, err)
        except IOError:
            Utilities.log(Utilities.logging.ERROR, "There is no required file to retrieve instances in given path.")
        except SyntaxError as err:
            Utilities.log(Utilities.logging.ERROR, err)

    def load_config(self):
        """
        Load configuration file to instance variables
        @return void
        """
        try:
            self.host_file = PARENT_DIR + Utilities.config_get("files", "host_file")
            self.instance_file = PARENT_DIR + Utilities.config_get("files", "instance_file")
            self.target_file = PARENT_DIR + Utilities.config_get("files", "target_file")
        except KeyError:
            Utilities.log(Utilities.logging.CRITICAL, "Required file(s) key could be found on configuration file.")
        except BaseException as exception:
            Utilities.log(Utilities.logging.CRITICAL, str(exception))

    @classmethod
    def check_file(cls, content_to_check):
        """
        This method check file content is regular or malformed.
        @param file_to_check
        @return Boolean True or False
        """
        # Pattern to check file content for provided files
        pattern = re.compile("^(?:[0-9]+,[0-9]+,[0-9]+\\r\\n)*[0-9]+,[0-9]+,[0-9]+$")
        try:
            if pattern.match(content_to_check):
                return True
            else:
                return False
        except RuntimeError:
            Utilities.log(Utilities.logging.ERROR, traceback.format_exc())
            return False

    def run(self):
        """
        Statistics instance runner

        It is not a thread but i like it to pretend as a thread
        @return void
        """
        # First fill hosts
        try:
            self.write_target(
                self.calculate_content(
                    data_centers=self.fill_data_centers(self.host_file)
                )
            )
            return True
        except SyntaxError as err:
            Utilities.log(Utilities.logging.CRITICAL, err)
        except BaseException:
            Utilities.log(Utilities.logging.CRITICAL, traceback.format_exc())
            return False

    def write_target(self, content=None):
        """
        Write calculated content into target file
        @param content which, will be calculated and written in the target file
        @return void
        """
        try:
            if content:
                with open(self.target_file, "w+") as target:
                    for line in content:
                        target.write("%s\n" % line)
                return True
            else:
                print "Error occurred while running the process. Please see log files."
        except IOError:
            Utilities.log(Utilities.logging.ERROR, "Destination file can not be opened to write.")
        except EOFError as err:
            Utilities.log(Utilities.logging.ERROR, err)
        except TypeError as err:
            Utilities.log(Utilities.logging.ERROR, err)

    def calculate_content(self, data_centers=None):
        """
        Calculate the content by given parameters regarding algorithm
        @param data_centers
        @rtype : a list including formatted data
        @return Object which includes:
         customer with the largest fraction of their total fleet of instances on a single host and output
         the value of that fraction;
         customer with the largest fraction of their total fleet of instances in a single data centre and output
         the value of that fraction;
         a list of all the hosts which have at least one empty slot.
        """
        try:
            # Host clustering pattern
            host_clustering = "HostClustering: %(customer_id)s, %(fraction).2f"
            max_host = {"fraction": 0, "customer_id": None}

            # Data center clustering pattern
            data_centre_clustering = "DatacentreClustering: %(customer_id)s, %(fraction).2f"
            max_center = {"fraction": 0, "customer_id": None}

            # Available hosts list pattern & host
            available_hosts = "AvailableHosts: "
            available_hosts_list = []

            # Calculate fraction for customer and hosts and find available hosts
            for center in data_centers:
                # Fraction of a host it starts with 1 because it has no effect when getting fraction
                # but it has to start with 1 by counting customers who have instance(s) on host/ data center
                fraction_of_host = 1

                # It is used to get total number of slots in a data center even though we know number of slots
                # in a single host but not data center
                max_number_of_slots = 0

                # Dictionary to keep number of instances which, belong to a single customer
                # This structure keeps values as a key=>value pair etc: {'9': 2, '13': 3, '16': 1}
                number_of_instance = {}

                # Loop in hosts including by data center
                for host in data_centers[center]:
                    tmp_val = 0
                    # Find available hosts
                    if int(data_centers[center][host]["number_of_slots"]) - len(
                            data_centers[center][host]["instances"]) > 0:
                        # Append the hosts that has an empty slot on it
                        available_hosts_list.append(host)
                    # Find largest fraction of total fleet of instances on a single host
                    for instance in data_centers[center][host]["instances"]:
                        # If current customer id is same with previous one increase fraction count
                        if instance["customer_id"] == tmp_val:
                            fraction_of_host += 1
                            # Calculate fraction if one customer has more than one instance on a single host then
                            fraction = float(fraction_of_host / int(data_centers[center][host]["number_of_slots"]))

                            # Check if recorded fraction is smaller than new one and then
                            if max_host["fraction"] < fraction:
                                # Set new one as recorded maximum fraction
                                max_host["fraction"] = fraction
                                # And get customer id who, has largest fraction
                                max_host["customer_id"] = instance["customer_id"]

                        # Set recent customer id to tmp to check following one with this
                        tmp_val = instance["customer_id"]

                        # Get total number of instances from a data center
                        if instance["customer_id"] in number_of_instance:
                            number_of_instance[instance["customer_id"]] += 1
                        else:
                            number_of_instance[instance["customer_id"]] = 1
                    # Find largest fraction of total flees ot instances on a single data center
                    max_number_of_slots += int(data_centers[center][host]["number_of_slots"])

                # Calculate largest fraction by given values on a single data center
                fraction = float(max(number_of_instance.iteritems(), key=operator.itemgetter(1))[1] / max_number_of_slots)
                # Check which one is larger and find max one
                if max_center["fraction"] < fraction:
                    max_center["fraction"] = fraction
                    # Find maximum value of iteration items in total number of instances
                    max_center["customer_id"] = max(number_of_instance.iteritems(), key=operator.itemgetter(1))[0]

            # Make a response body to use it anywhere
            response = []

            # Join available host into a single string
            available_hosts += ",".join(available_hosts_list)

            # Format patterns by calculated values
            response.append(host_clustering % max_host)
            response.append(data_centre_clustering % max_center)
            response.append(available_hosts)

            # return response as a list
            return response
        except BaseException:
            Utilities.log(Utilities.logging.ERROR, traceback.format_exc())


if __name__ == "__main__":
    # Create an instance of Statistics object
    statistics = Statistics()
    # Then run it!
    statistics.run()
