# Phone Number Location Tracker

A Python application that tracks and displays detailed location information for phone numbers, including state, district, city, and service provider details.

## Features

- 📍 **Detailed Location Information**: Country, State, District, City, and Postcode
- 📱 **Phone Number Details**: Service Provider, Number Type, Timezone
- 🗺️ **Interactive Map**: Generates an HTML map showing the phone number's location
- ✅ **Number Validation**: Checks if the number is valid and possible
- 🌐 **Geocoding**: Uses OpenCage API for accurate location data

## Requirements

- Python 3.x
- phonenumbers library
- folium library
- opencage library

## Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install phonenumbers
pip install folium
pip install opencage
```

## Setup

1. Get a free API key from [OpenCage Geocoding API](https://opencagedata.com/)
2. Replace the `Key` variable in `track_phonenumber.py` with your API key:
```python
Key = "your_opencage_api_key_here"
```

## Usage

1. Run the script:
```bash
python track_phonenumber.py
```

2. Enter a phone number with country code when prompted:
```
Example: +919876543210
```

3. The script will display:
   - General location (country/region)
   - Service provider name
   - Timezone
   - Number type (Mobile, Fixed Line, VoIP, etc.)
   - Detailed location information (State, District, City)
   - Coordinates (Latitude, Longitude)

4. An interactive map (`mylocation.html`) will be generated automatically

## Output Information

### Console Output
- **General Location**: Broad location based on phone number
- **Service Provider**: Telecom carrier (e.g., Reliance Jio, Airtel)
- **Timezone**: Time zone(s) for the number
- **Number Type**: Mobile, Fixed Line, VoIP, etc.
- **Validation**: Whether the number is valid and possible
- **Detailed Location**:
  - Country
  - State/Region
  - District
  - City/Town
  - Postcode
  - Full formatted address

### Map Output
- Interactive HTML map saved as `mylocation.html`
- Marker showing the approximate location
- Popup with detailed location information
- Can be opened in any web browser

## Important Notes

⚠️ **Privacy & Legal Considerations**:
- This tool is for educational purposes only
- Phone number location is approximate and based on publicly available data
- Does NOT provide exact street addresses or personal information
- Respect privacy laws and use responsibly

⚠️ **Accuracy**:
- Location accuracy depends on the phone number's country code and format
- Results show the general region/city, not exact locations
- Mobile numbers typically reveal less precise locations than fixed lines

## Example

```
Enter phone number with country code: +919876543210

General Location: India
Service Provider: Reliance Jio
Timezone(s): Asia/Calcutta
Number Type: Mobile
Valid Number: True
Possible Number: True

==================================================
DETAILED LOCATION INFORMATION
==================================================
Country: India
State/Region: Maharashtra
State District: Mumbai
City: Mumbai
Postcode: 400001
Formatted Address: Mumbai, Maharashtra, India
==================================================

Map saved to 'mylocation.html'
```

## Troubleshooting

### Import Errors
If you get import errors, make sure all packages are installed:
```bash
pip install --upgrade phonenumbers folium opencage
```

### API Key Issues
- Ensure your OpenCage API key is valid
- Free tier has a limit of 2,500 requests per day
- Check your API key at https://opencagedata.com/dashboard

### No Results
- Verify the phone number includes the country code (e.g., +91 for India)
- Check if the phone number format is correct
- Some numbers may not have detailed location data available

## License

This project is for educational purposes only. Use responsibly and ethically.

## Disclaimer

This tool does not provide personal information about phone number owners. It only shows general location information based on the phone number's area code and publicly available geocoding data.
