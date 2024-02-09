import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



def camel_to_snake(name):
    """
    Converts a given string from CamelCase to snake_case.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


@transformer
def transform(data, *args, **kwargs):
    
    print("Rows with zero passengers: ", data['passenger_count'].isin([0]).sum())
    print("Rows with zero trip distance: ", data['trip_distance'].isin([0]).sum())
    #load only data > 0 for passengeer_count and trip_distance
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

    if data['lpep_pickup_datetime'].dtype != '<M8[ns]':  # <M8[ns] is numpy datetime64
        data['lpep_pickup_datetime'] = pd.to_datetime(data['lpep_pickup_datetime'])
    
    # Create lpep_pickup_date column by extracting the date from lpep_pickup_datetime
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    # Rename columns from CamelCase to snake_case
    data.columns = [camel_to_snake(col) for col in data.columns]

    return data


@test
def test_output(output, *args) -> None:

    assert output is not None, 'The output is undefined'
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'        
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with zero trip distance'        
    assert output['lpep_pickup_date'].dtype == object, 'Column lpep_pickup_date is not of type object (date)'
    assert 'vendor_id' in output.columns, 'Column vendor_id not found after renaming'