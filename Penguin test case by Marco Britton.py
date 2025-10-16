# Project: SI 201 - Fall 2025 Project 1
# Student Name: Marco Britton
# Student ID: [47102184]
# Email: [Brimarco@umich.edu]
# Dataset: Palmer Penguins (Kaggle)
# Collaborators: Used ChatGPT (GPT-5) for code debugging and explanation.
# Functions Created By: Marco Britton

import unittest
import os
import csv


def load_penguins(f):
    '''
    Params:
        f (str): filename or path of the penguin CSV file.

    Returns:
        dict: species → list of measurement dicts
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
            species = row['species'].strip().capitalize()  # normalize capitalization and spaces
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
        d (dict): species → list of measurement dicts

    Returns:
        dict: species → dict of averaged measurements (floats rounded to 2 decimals)
    '''
    averages = {}

    for species, entries in d.items():
        # filter out empty or 'NA' values before converting
        bills = [float(e['bill_length_mm']) for e in entries 
                 if e['bill_length_mm'] and e['bill_length_mm'].upper() != 'NA']
        flippers = [float(e['flipper_length_mm']) for e in entries 
                    if e['flipper_length_mm'] and e['flipper_length_mm'].upper() != 'NA']
        masses = [float(e['body_mass_g']) for e in entries 
                  if e['body_mass_g'] and e['body_mass_g'].upper() != 'NA']

        # skip if all are missing
        if not bills and not flippers and not masses:
            continue

        species_avg = {}
        if bills:
            species_avg['bill_length_mm'] = round(sum(bills) / len(bills), 2)
        if flippers:
            species_avg['flipper_length_mm'] = round(sum(flippers) / len(flippers), 2)
        if masses:
            species_avg['body_mass_g'] = round(sum(masses) / len(masses), 2)

        if species_avg:
            averages[species] = species_avg

    return averages




def print_species_averages(averages):
    '''
    Prints the average measurements for all penguin species.
    '''
    print("\n📊 Average Measurements by Species:")
    print("===================================")
    for species, vals in averages.items():
        print(f"{species}:")
        print(f"  Bill Length (mm):   {vals['bill_length_mm']}")
        print(f"  Flipper Length (mm): {vals['flipper_length_mm']}")
        print(f"  Body Mass (g):      {vals['body_mass_g']}\n")


def save_averages_to_csv(averages, filename='penguin_averages.csv'):
    '''
    Saves the computed species averages to a CSV file.
    '''
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['species', 'bill_length_mm', 'flipper_length_mm', 'body_mass_g'])
        for species, vals in averages.items():
            writer.writerow([
                species,
                vals['bill_length_mm'],
                vals['flipper_length_mm'],
                vals['body_mass_g']
            ])
    print(f"✅ Averages saved to {filename}")


# ====================== UNIT TESTS ======================

class penguin_test(unittest.TestCase):
    '''
    Unit tests for penguin data functions.
    '''

    def setUp(self):
        self.penguin_dict = load_penguins('penguins.csv')
        self.avg_dict = get_species_averages(self.penguin_dict)

    def test_load_penguins(self):
        self.assertIn('Adelie', self.penguin_dict)
        example = self.penguin_dict['Adelie'][0]
        self.assertIn('bill_length_mm', example)
        self.assertIn('flipper_length_mm', example)
        self.assertIn('body_mass_g', example)

    def test_get_species_averages(self):
        for species, vals in self.avg_dict.items():
            self.assertTrue(all(isinstance(v, float) for v in vals.values()))
            self.assertTrue(all(v > 0 for v in vals.values()))

        # sanity check
        if 'Gentoo' in self.avg_dict and 'Adelie' in self.avg_dict:
            self.assertGreater(
                self.avg_dict['Gentoo']['body_mass_g'],
                self.avg_dict['Adelie']['body_mass_g']
            )

    def test_empty_species(self):
        empty_dict = {'FakeSpecies': []}
        result = get_species_averages(empty_dict)
        self.assertEqual(result, {})

    def test_missing_values(self):
        test_dict = {'Adelie': [{'bill_length_mm': '', 'flipper_length_mm': '190', 'body_mass_g': '3700'}]}
        result = get_species_averages(test_dict)
        self.assertIn('Adelie', result)


# ====================== MAIN EXECUTION ======================

def main():
    # Run tests first
    unittest.main(exit=False, verbosity=2)

    # After tests, print and save averages
    penguin_dict = load_penguins('penguins.csv')
    avg_dict = get_species_averages(penguin_dict)
    print_species_averages(avg_dict)
    save_averages_to_csv(avg_dict)


if __name__ == '__main__':
    main()
