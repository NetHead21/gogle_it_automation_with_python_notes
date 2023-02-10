#!/usr/bin/env python3
import csv
from pprint import pprint


def read_employees(csv_file_location):
    csv.register_dialect('empDialect', skipinitialspace=True, strict=True)
    employee_file = csv.DictReader(
        open(csv_file_location), dialect='empDialect')
    return list(employee_file)


def process_data(employee_list):
    department_list = [
        employee_data['Department'] for employee_data in employee_list
    ]
    return {
        department_name: department_list.count(department_name)
        for department_name in set(department_list)
    }


def write_report(dictionary, report_file):
    with open(report_file, "w+") as f:
        for k in sorted(dictionary):
            f.write(str(k)+':'+str(dictionary[k])+'\n')
        f.close()


employees = r"./data/employees.csv"
employee_list = read_employees(employees)

dictionary = process_data(employee_list)
print(dictionary)

write_report(dictionary, './data/report.txt')
