import csv,os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./api_key.json"

from time import sleep

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Filter,
    FilterExpression,
    Metric,
    RunReportRequest,
)


def run_report(property_id="YOUR-GA4-PROPERTY-ID"):
    """Runs a simple report on a Google Analytics 4 property."""
    # TODO(developer): Uncomment this variable and replace with your
    #  Google Analytics 4 property ID before running the sample.
    # property_id = "YOUR-GA4-PROPERTY-ID"

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="eventCount")],
        #date_ranges=[DateRange(start_date="2020-03-31", end_date="today")],
        date_ranges=[DateRange(start_date="90daysAgo", end_date="today")],
        dimension_filter=FilterExpression(
                filter=Filter(
                    field_name="pagePath",
                    string_filter=Filter.StringFilter(
                        match_type=Filter.StringFilter.MatchType.CONTAINS,
                        value="@"
                    ),
                )
        ),
    )
    response = client.run_report(request)

    print("Report result:")
    for row in response.rows:
        print(row.dimension_values[0].value, row.metric_values[0].value)

def run_report_from_csv(csv_obj,search_string="@"):
    #print(csv_obj)

    account_id = csv_obj[1]
    property_id = csv_obj[3]
    property_number = property_id[11:]
    dimension = csv_obj[5]
    scope = csv_obj[6]
    dimension_prefix = ""
    if "USER" in scope: 
        dimension_prefix = "customUser:"
    if "EVENT" in scope:     
        dimension_prefix = "customEvent:"
    
    #print(f"Analyzing dimension {dimension} in property {property_id}")
    """Runs a simple report on a Google Analytics 4 property based on input from a CSV file"""
    # TODO(developer): Uncomment this variable and replace with your
    #  Google Analytics 4 property ID before running the sample.
    # property_id = "YOUR-GA4-PROPERTY-ID"

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=property_id,
        dimensions=[
            Dimension(name="pagePath"),
            Dimension(name=dimension_prefix+dimension)
        ],
        metrics=[Metric(name="eventCount")],
        #date_ranges=[DateRange(start_date="2020-03-31", end_date="today")],
        date_ranges=[DateRange(start_date="90daysAgo", end_date="today")],
        dimension_filter=FilterExpression(
                filter=Filter(
                    field_name=dimension_prefix+dimension,
                    string_filter=Filter.StringFilter(
                        match_type=Filter.StringFilter.MatchType.CONTAINS,
                        value=search_string
                    ),
                )
        ),
    )
    response = client.run_report(request)

    if response.rows:
        #print("Report result:")
        #print(response.rows)
        f = open("./potential_pii_ga4.csv", "a")
        for row in response.rows:
            output_string= f"{property_number},{dimension},{row.dimension_values[0].value},{row.dimension_values[1].value}"
            f.write(output_string+"\n")
            #print(property_number,dimension, row.dimension_values[0].value, row.dimension_values[1].value)
        f.close()

""" Going through CSV """
filename = "./ga4_dims.csv"
with open(filename) as file_obj:
    #lines = len(file_obj.readlines())
    reader_obj = csv.reader(file_obj)
    i = 0
    for row in reader_obj:
        i = i +1
        if i>10005:
            sleep(0.02)
            print(row)
            run_report_from_csv(row)
        