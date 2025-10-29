# In src/services/image_generator.py
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from typing import List, Dict
import os


def generate_summary_image(
    total_countries: int,
    top_countries: List[Dict],
    last_refresh: datetime,
    output_path: str = "cache/summary.png",
):
    """Generate a summary image with country statistics"""

    # Create cache directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Image dimensions
    width = 800
    height = 600

    # Create image with white background
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.load_default()
    header_font = ImageFont.load_default()
    text_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

    # Colors
    primary_color = (41, 128, 185)
    secondary_color = (52, 73, 94)
    accent_color = (46, 204, 113)
    text_color = (44, 62, 80)

    # Draw header background
    draw.rectangle([(0, 0), (width, 100)], fill=primary_color)

    # Draw title
    title = "Countries Summary Report"
    draw.text((width // 2, 50), title, fill="white", font=title_font, anchor="mm")

    # Draw total countries
    y_offset = 130
    total_text = f"Total Countries: {total_countries}"
    draw.text((50, y_offset), total_text, fill=accent_color, font=header_font)

    # Draw top 5 countries header
    y_offset += 60
    draw.text(
        (50, y_offset),
        "Top 5 Countries by GDP:",
        fill=secondary_color,
        font=header_font,
    )

    # Draw top countries list
    y_offset += 40
    for i, country in enumerate(top_countries, 1):
        country_name = country.get("name", "Unknown")
        gdp = country.get("estimated_gdp", 0)

        # Format GDP with commas
        gdp_formatted = f"${gdp:,.2f}" if gdp else "N/A"

        country_text = f"{i}. {country_name}"
        gdp_text = f"{gdp_formatted}"

        draw.text((70, y_offset), country_text, fill=text_color, font=text_font)
        draw.text((500, y_offset), gdp_text, fill=primary_color, font=text_font)

        y_offset += 35

    # Draw timestamp at the bottom
    y_offset = height - 60
    if last_refresh:
        timestamp_text = f"Last Refreshed: {last_refresh}"
    else:
        timestamp_text = "Last Refreshed: Never"

    draw.text(
        (width // 2, y_offset),
        timestamp_text,
        fill=secondary_color,
        font=small_font,
        anchor="mm",
    )

    # Draw footer line
    draw.line(
        [(50, height - 40), (width - 50, height - 40)], fill=primary_color, width=2
    )

    # Save image
    img.save(output_path, quality=95)
    print(f"Summary image saved to {output_path}")
