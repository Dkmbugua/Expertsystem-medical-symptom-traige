"""
Hospital Data Validator and Enhancer

Senior Dev Tool:
- Validates all hospital coordinates
- Fills missing coordinates via geocoding
- Adds reverse-geocoded addresses
- Generates data quality report
"""

import sqlite3
import logging
from location_service import location_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_and_enhance_hospitals():
    """
    Validate and enhance hospital data with coordinates and addresses
    """
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Get all hospitals
    cursor.execute("SELECT id, name, address, latitude, longitude, contact FROM hospitals")
    hospitals = cursor.fetchall()
    
    stats = {
        'total': len(hospitals),
        'valid_coords': 0,
        'missing_coords': 0,
        'geocoded': 0,
        'enhanced_address': 0,
        'errors': 0
    }
    
    logger.info(f"Validating {stats['total']} hospitals...")
    
    for hospital_id, name, address, lat, lon, contact in hospitals:
        try:
            # Check if coordinates exist and are valid
            if lat and lon and location_service.validate_coordinates(lat, lon):
                stats['valid_coords'] += 1
                
                # Enhance address if missing
                if not address:
                    logger.info(f"Enhancing address for {name}...")
                    enhanced_address = location_service.reverse_geocode(lat, lon)
                    if enhanced_address:
                        cursor.execute(
                            "UPDATE hospitals SET address = ? WHERE id = ?",
                            (enhanced_address, hospital_id)
                        )
                        stats['enhanced_address'] += 1
                        logger.info(f"  ✓ Added address: {enhanced_address}")
            else:
                stats['missing_coords'] += 1
                logger.warning(f"Missing/invalid coordinates for {name}")
                
                # Try to geocode from address or name
                search_term = address if address else name
                if search_term:
                    logger.info(f"Geocoding {name}...")
                    result = location_service.geocode(search_term)
                    if result:
                        cursor.execute(
                            "UPDATE hospitals SET latitude = ?, longitude = ?, address = ? WHERE id = ?",
                            (result['lat'], result['lon'], result['formatted_address'], hospital_id)
                        )
                        stats['geocoded'] += 1
                        logger.info(f"  ✓ Added coordinates: {result['lat']}, {result['lon']}")
                    else:
                        logger.error(f"  ✗ Could not geocode {name}")
                        stats['errors'] += 1
        
        except Exception as e:
            logger.error(f"Error processing {name}: {e}")
            stats['errors'] += 1
    
    conn.commit()
    conn.close()
    
    # Print report
    print("\n" + "="*60)
    print("HOSPITAL DATA QUALITY REPORT")
    print("="*60)
    print(f"Total hospitals:           {stats['total']}")
    print(f"Valid coordinates:         {stats['valid_coords']} ✓")
    print(f"Missing coordinates:       {stats['missing_coords']}")
    print(f"Successfully geocoded:     {stats['geocoded']} ✓")
    print(f"Enhanced addresses:        {stats['enhanced_address']} ✓")
    print(f"Errors:                    {stats['errors']}")
    print("="*60)
    print(f"\nData Quality: {(stats['valid_coords'] + stats['geocoded']) / stats['total'] * 100:.1f}%")
    print("\n")


if __name__ == '__main__':
    validate_and_enhance_hospitals()
