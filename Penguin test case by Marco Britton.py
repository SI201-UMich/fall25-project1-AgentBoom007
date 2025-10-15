# Student Name: Marco Britton
# Student ID: 47102184 
# Email: Brimarco@umich.edu
# Collaborators:Gen AI ChatGPT


import unittest
import os
import csv

def load_penguins(f):
    '''
    Params: 
        f, name or path of CSV file (string)

    Returns:
        dict of species → list of dicts containing measurements
        Example:
        {
          'Adelie': [{'bill_length_mm': '39.1', 'flipper_length_mm': '181', 'body_mass_g': '3750'}, ...],
          'Gentoo': [{'bill_length_mm': '47.6', 'flipper_length_mm': '214', 'body_mass_g': '5050'}, ...]
        }
    '''
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, f)

    data = {}
    with open(full_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Normalize species names to avoid spacing/case mismatches
            species = row['species'].strip().capitalize()
            if species not in data:
                data[species] = []
            data[species].append({
                'bill_length_mm': row['bill_length_mm'],
                'flipper_length_mm': row['flipper_length_mm'],
                'body_mass_g': row['body_mass_g']
            })
    return data


def get_species_averages(d):
    '''
    Params:
        d, dict from load_penguins

    Returns:
        dict where each key is a species name,
        and each value is a dict with the averages (rounded to 2 decimals):
        {
          'Adelie': {'bill_length_mm': 38.79, 'flipper_length_mm': 189.95, 'body_mass_g': 3700.66},
          ...
        }
    '''
    averages = {}
    for species, entries in d.items():
        try:
            # Convert numeric strings to floats
            bills = [float(e['bill_length_mm']) for e in entries if e['bill_length_mm']]
            flippers = [float(e['flipper_length_mm']) for e in entries if e['flipper_length_mm']]
            masses = [float(e['body_mass_g']) for e in entries if e['body_mass_g']]

            avg_bill = round(sum(bills) / len(bills), 2)
            avg_flipper = round(sum(flippers) / len(flippers), 2)
            avg_mass = round(sum(masses) / len(masses), 2)

            averages[species] = {
                'bill_length_mm': avg_bill,
                'flipper_length_mm': avg_flipper,
                'body_mass_g': avg_mass
            }

        except (ValueError, ZeroDivisionError):
            continue

    return averages


def print_species_averages(averages):
    '''
    Prints formatted averages for all species.
    '''
    print("\n📊 Average Measurements by Species:")
    print("===================================")
    for species, vals in averages.items():
        print(f"{species}:")
        print(f"  Bill Length (mm):   {vals['bill_length_mm']}")
        print(f"  Flipper Length (mm): {vals['flipper_length_mm']}")
        print()


class penguin_test(unittest.TestCase):
    '''
    Test cases for penguin dataset.
    '''

    def setUp(self):
        # assumes penguins.csv exists in same directory
        self.penguin_dict = load_penguins('penguins.csv')
        self.avg_dict = get_species_averages(self.penguin_dict)

    def test_load_penguins(self):
        # Outer keys should be species
        self.assertIn('Adelie', self.penguin_dict)
        # Check one measurement
        example = self.penguin_dict['Adelie'][0]
        self.assertIn('bill_length_mm', example)
        self.assertIn('flipper_length_mm', example)
        self.assertIn('body_mass_g', example)

    def test_get_species_averages(self):
        # Make sure averages are numbers and positive
        for species, vals in self.avg_dict.items():
            self.assertTrue(all(isinstance(v, float) for v in vals.values()))
            self.assertTrue(all(v > 0 for v in vals.values()))
        # Example check: Gentoo penguins should have higher average body mass than Adelie
        if 'Gentoo' in self.avg_dict and 'Adelie' in self.avg_dict:
            self.assertGreater(self.avg_dict['Gentoo']['body_mass_g'],
                               self.avg_dict['Adelie']['body_mass_g'])


def main():
    # Run unit tests
    unittest.main(exit=False, verbosity=2)

    # After tests, print all species averages
    penguin_dict = load_penguins('penguins.csv')
    avg_dict = get_species_averages(penguin_dict)
    print_species_averages(avg_dict)


if __name__ == '__main__':
    main()
