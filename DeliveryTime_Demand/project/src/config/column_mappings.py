"""Configuration for dataset column mappings."""

# Original column names from dataset
COLUMNS = {
    'DELIVERY_PERSON': 'Delivery_person_ID',
    'AGE': 'Delivery_person_Age',
    'RATINGS': 'Delivery_person_Ratings',
    'RESTAURANT_LAT': 'Restaurant_latitude',
    'RESTAURANT_LNG': 'Restaurant_longitude',
    'DELIVERY_LAT': 'Delivery_location_latitude',
    'DELIVERY_LNG': 'Delivery_location_longitude',
    'ORDER_DATE': 'Order_Date',
    'ORDER_TIME': 'Time_Orderd',
    'PICKUP_TIME': 'Time_Order_picked',
    'WEATHER': 'Weatherconditions',
    'TRAFFIC': 'Road_traffic_density',
    'VEHICLE_CONDITION': 'Vehicle_condition',
    'ORDER_TYPE': 'Type_of_order',
    'VEHICLE_TYPE': 'Type_of_vehicle',
    'MULTIPLE_DELIVERIES': 'multiple_deliveries',
    'FESTIVAL': 'Festival',
    'CITY': 'City'
}

# Encoded column names
ENCODED_COLUMNS = {
    'Weatherconditions': 'Weather_encoded',
    'Road_traffic_density': 'Traffic_encoded',
    'Type_of_vehicle': 'Vehicle_encoded',
    'Type_of_order': 'Order_type_encoded',
    'Festival': 'Festival_encoded',
    'City': 'City_encoded'
}