import os
from google.analytics.admin import AnalyticsAdminServiceClient

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./api_key.json"

def list_accounts(transport: str = None):
    """
    Lists the available Google Analytics accounts.

    Args:
        transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
    """
    

    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = AnalyticsAdminServiceClient(transport=transport)

    results = client.list_accounts()

    # Displays the configuration information for all Google Analytics accounts
    # available to the authenticated user.
    for account in results:
        #print(account)
        print(account.name+','+account.display_name)

def list_summaries(transport: str = None):
    """
    Prints summaries of all accounts accessible by the caller.

    Args:
        transport(str): The transport to use. For example, "grpc"
            or "rest". If set to None, a transport is chosen automatically.
    """
    client = AnalyticsAdminServiceClient(transport=transport)
    results = client.list_account_summaries()

    for account_summary in results:
        for property_summary in account_summary.property_summaries:
            # property_data_retention = client.get_data_retention_settings(name=f'{property_summary.property}/dataRetentionSettings')
            # print(f"{account_summary.account},{account_summary.display_name},{property_summary.property},{property_summary.display_name},{property_data_retention.event_data_retention},{property_data_retention.reset_user_data_on_new_activity}")
            cdims = client.list_custom_dimensions(parent=f'{property_summary.property}')
            
            for dim in cdims:
                print (f"{dim.name},"+str(dim.scope))
                exit()    
                print(f"{account_summary.display_name},{account_summary.account},{property_summary.display_name},{property_summary.property},{dim.name},{dim.parameter_name},"+dim.scope)
                
list_summaries()
