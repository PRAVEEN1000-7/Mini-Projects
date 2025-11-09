import phonenumbers
from phonenumbers import geocoder, carrier, timezone
#from test import number
import folium

Key = "opencage_api_key"

number = input("Enter phone number with country code:")
check_number = phonenumbers.parse(number)

# Get basic location
number_location = geocoder.description_for_number(check_number, "en")
print(f"\nGeneral Location: {number_location}")

# Get service provider
service_provider = phonenumbers.parse(number)
service_name = carrier.name_for_number(service_provider, "en")
print(f"Service Provider: {service_name}")

# Get timezone
timezones = timezone.time_zones_for_number(check_number)
print(f"Timezone(s): {', '.join(timezones) if timezones else 'N/A'}")

# Get number type and validity
n_type = phonenumbers.number_type(check_number)
# NumberType enum values
type_mapping = {
    0: "Fixed Line",
    1: "Mobile",
    2: "Fixed Line or Mobile",
    3: "Toll Free",
    4: "Premium Rate",
    5: "Shared Cost",
    6: "VoIP",
    7: "Personal Number",
    8: "Pager",
    9: "UAN",
    10: "Voicemail",
    -1: "Unknown"
}
print(f"Number Type: {type_mapping.get(n_type, 'Unknown')}")
print(f"Valid Number: {phonenumbers.is_valid_number(check_number)}")
print(f"Possible Number: {phonenumbers.is_possible_number(check_number)}")

from opencage.geocoder import OpenCageGeocode
geocoder = OpenCageGeocode(Key)

query = str(number_location)
results = geocoder.geocode(query)

# Extract coordinates
lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']
print(f"\nCoordinates: {lat}, {lng}")

# Extract detailed location information
components = results[0]['components']
formatted_address = results[0]['formatted']

print("\n" + "="*50)
print("DETAILED LOCATION INFORMATION")
print("="*50)

# Display available location details
print(f"Country: {components.get('country', 'N/A')}")
print(f"State/Region: {components.get('state', components.get('region', 'N/A'))}")
print(f"State District: {components.get('state_district', 'N/A')}")
print(f"County: {components.get('county', 'N/A')}")
print(f"City: {components.get('city', components.get('town', components.get('village', 'N/A')))}")
print(f"Postcode: {components.get('postcode', 'N/A')}")
print(f"Formatted Address: {formatted_address}")

# Additional information if available
if 'suburb' in components:
    print(f"Suburb/Locality: {components['suburb']}")
if 'neighbourhood' in components:
    print(f"Neighbourhood: {components['neighbourhood']}")
if 'road' in components:
    print(f"Road: {components['road']}")

print("="*50)

# Create detailed popup text
popup_text = f"""
<b>Phone Number Location</b><br>
Country: {components.get('country', 'N/A')}<br>
State: {components.get('state', components.get('region', 'N/A'))}<br>
District: {components.get('state_district', 'N/A')}<br>
City: {components.get('city', components.get('town', components.get('village', 'N/A')))}<br>
Coordinates: {lat}, {lng}
"""

# Create map with detailed marker
map_location = folium.Map(location=[lat, lng], zoom_start=9)
folium.Marker([lat, lng], popup=folium.Popup(popup_text, max_width=300), 
              tooltip=number_location).add_to(map_location)
map_location.save("mylocation.html")

print(f"\nMap saved to 'mylocation.html'")
print(f"Service Provider: {carrier.name_for_number(service_provider, 'en')}")