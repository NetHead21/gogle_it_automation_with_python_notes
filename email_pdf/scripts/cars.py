#!/usr/bin/env python3

import emails
import reports
import json
import locale
import sys
import collections
import operator
import os

# import os.path


def load_data(filename):
    """Loads the contents of filename as a JSON file."""
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def format_car(car):
    """Given a car dictionary, returns a nicely formatted name."""
    return f'{car["car_make"]} {car["car_model"]} ({car["car_year"]})'


def process_data(data):
    """Analyzes the data, looking for maximums.

    Returns a list of lines that summarize the information.
    """
    locale.setlocale(locale.LC_ALL, "C.UTF-8")
    max_revenue = {"revenue": 0}
    max_sales = {"total_sales": 0}
    car_year_sales = collections.defaultdict(int)
    for item in data:
        # Calculate the revenue generated by this model (price * total_sales)
        # We need to convert the price from "$1234.56" to 1234.56
        item_price = locale.atof(item["price"].strip("$"))
        item_revenue = item["total_sales"] * item_price
        if item_revenue > max_revenue["revenue"]:
            item["revenue"] = item_revenue
            max_revenue = item

        """
    1. Calculate the car model which had the most sales by completing the process_data method, 
    and then appending a formatted string to the summary list in the below format:
        * "The {car model} had the most sales: {total sales}"
    2. Calculate the most popular car_year across all car make/models (in other words, find the total count of cars with the car_year equal to 2005, equal to 2006, etc. and then figure out the most popular year) 
    by completing the process_data method, and append a formatted string to the summary list in the below format:
        * "The most popular year was {year} with {total sales in that year} sales."
    """

        # TODO: also handle max sales
        if item["total_sales"] > max_sales["total_sales"]:
            max_sales = item

        car_year_sales[item["car"]["car_year"]] += item["total_sales"]

    # TODO: also handle most popular car_year
    popular_car_year = max(car_year_sales.items(), key=operator.itemgetter(1))
    pop_year, pop_sales = popular_car_year

    return [
        f'The {format_car(max_revenue["car"])} generated the most revenue: ${max_revenue["revenue"]}',
        f'The {format_car(max_sales["car"])} had the most sales: {max_sales["total_sales"]}',
        f"The most popular year was {pop_year} with {pop_sales} sales.",
    ]


def cars_dict_to_table(car_data):
    """Turns the data in car_data into a list of lists."""
    table_data = [["ID", "Car", "Price", "Total Sales"]]
    table_data.extend(
        [
            item["id"],
            format_car(item["car"]),
            item["price"],
            item["total_sales"],
        ]
        for item in car_data
    )
    return table_data


def main(argv):
    """Process the JSON data and generate a full report out of it."""
    data = load_data("car_sales.json")
    # data = load_data(os.path.expanduser('~') + "/car_sales.json")
    summary = process_data(data)

    """
    The PDF should contain:

        * A summary paragraph which contains the most sales/most revenue/most popular year values worked out in the previous step.
        Note: To add line breaks in the PDF, use: <br/> between the lines.
        * A table which contains all the information parsed from the JSON file, organised by id_number. The car details should be combined into one column in the form <car_make> <car_model> (<car_year>).
        Note: You can use the cars_dict_to_table function for the above task.
    """

    # TODO: turn this into a PDF report
    filename = "/tmp/cars.pdf"
    title = "Sales summary for last month"
    additional_info = "<br/>".join(summary)
    table_data = cars_dict_to_table(data)
    reports.generate(filename, title, additional_info, table_data)
    # print("PDF OK") # test

    # TODO: send the PDF report as an email attachment
    sender = "automation@example.com"
    recipient = f'{os.environ.get("USER")}@example.com'
    subject = "Sales summary for last month"
    body = "\n".join(summary)
    attachment_path = "/tmp/cars.pdf"
    message = emails.generate(sender, recipient, subject, body, attachment_path)
    emails.send(message)
    # print("EMAIL OK") # test


if __name__ == "__main__":
    main(sys.argv)
