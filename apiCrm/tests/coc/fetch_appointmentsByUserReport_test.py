#!/usr/bin/env python
import asyncio
import logging
import json
from datetime import datetime, timedelta
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import the function we want to test
from apiCrm.resolvers.fetch_appointmentsByUserReport import fetch_and_process_appointmentsByUserReport

async def main():
    # Calculate date range for last 7 days
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=70)).strftime('%Y-%m-%d')
    
    print(f"Fetching appointments by user report from {start_date} to {end_date}...")
    
    # Call the function we want to test
    appointments = await fetch_and_process_appointmentsByUserReport(start_date, end_date)
    
    # Print summary of results
    print(f"Successfully fetched {len(appointments)} appointments")
    
    # Print first appointment as sample (if available)
    if appointments and len(appointments) > 0:
        print("\nSample appointment data:")
        print(json.dumps(appointments[0], indent=2, default=str))

if __name__ == "__main__":
    # Run the async function
    asyncio.run(main())