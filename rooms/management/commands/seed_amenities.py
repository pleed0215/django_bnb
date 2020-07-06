from django.core.management.base import BaseCommand
from rooms import models as rooms_models


class Command(BaseCommand):
    help = "This command will seed amenities for development."

    """
    def add_arguments(self, parser):
        parser.add_argument(
            "--times",
            default=50,
            type=int,
            help="How many dummy rooms do you want make?",
        )
    """

    def handle(self, *args, **options):
        amenities = [
            "Convenient",
            "Downtown",
            "LocationOn-Site",
            "RestaurantsOn-Site",
            "Retail",
            "SpacesSwimming",
            "PoolSun",
            "DeckControlled Access",
            "ParkingBike",
            "ParkingCommunity",
            "Lounge with Coffee",
            "Station24 Hour",
            "State-of-the-Art",
            "Fitness Center – Technogym Equippe",
            "Virtual Concierge App",
            "Security Access",
            "Pet-Friendly",
            "Grilling Pavilion",
            "Oversized Balconies Over Looking Pool",
            "Business Center",
            "Private Meeting Rooms",
            "Nest Thermostat",
            "USB Outlets",
            "Keyless Electronic Unit Entry",
            "Washer and Dryers in All Units",
            "Private Bedrooms and Bathrooms",
            "Stainless Steel Appliances",
            "Ceiling Fans in All Bedrooms",
            "TV Included",
            "Wi-Fi Included",
            "Utilities Included",
            "Quartz Countertops with Tile Backsplash",
            "Private Balconies and Patios",
            "Dining Room",
            "Clubhouse with Lounge Seating and HDTV Living Room",
            "Cyber Lounge with iMacs",
            "Conference Rooms",
            "Resort-Style Pools and Courtyard",
            "Screening Room with 128” Projector screen",
            "Online Payments",
            "Custom Cabinetry and Large Kitchen Islands",
            "Custom Colored Accent walls",
            "Dual Sinks",
            "Frameless Shower Doors",
            "Luxury Bathrooms with Natural Stone Countertops",
            "High Ceilings",
            "Oversized Oval Soaking Tubs",
            "Plush Carpeting in Bedrooms",
            "Spacious Walk-In Closets",
            "Wood-Style Flooring in Living and Dining Areas",
            "Computer Desks In Each Unit",
            "Roof-Top Terraces",
            "Fire Pits",
            "Movie Theater",
            "Toddler Room",
            "Sun Tanning Salon",
            "Multi-Purpose Game Room",
            "Spa",
            "Indoor Basketball",
            "Wine Cellar",
            "Gift Wrapping Station",
            "Feng Shui Parks",
            "Water Filtration",
            "Planting Garden",
            "Outdoor Showers",
            "Personal Tanning",
            "Hair and Nail Salons",
            "Bark Parks",
            "Library",
            "Food Shopping",
            "Sound-Proof Music JamRoom with Piano",
            "Greater Amounts of Storage",
            "Electric Car Charging Stations",
            "Recycling Service",
            "Valet Trash",
            "Golf Simulators",
            "Co-Working Spaces",
            "Living Green Walls",
            "Putting Green",
            "Lake",
            "Life-sized Chessboard",
            "Cooking Classes",
            "“Smart” Sensors that Control Lighting and Temperature",
            "Valet Parking",
            "Indoor Mail Boxes and Mobile Package Service Alerts",
        ]

        for a in amenities:
            rooms_models.Amenity.objects.create(name=a)
        self.stdout.write(
            self.style.SUCCESS(f"{len(amenities)} amenities succefully made.")
        )

