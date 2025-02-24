import schedule
import time
from datetime import datetime
from report_generator import ReportGenerator

def generate_scheduled_report():
    print(f"\nGenerating report at {datetime.now()}")
    generator = ReportGenerator()
    result = generator.create_report()
    print(result)

def main():
    print("Report Scheduler Started")
    print("Reports will be generated every 6 hours")
    
    # Schedule reports every 6 hours
    schedule.every(6).hours.do(generate_scheduled_report)
    
    # Generate initial report
    generate_scheduled_report()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
