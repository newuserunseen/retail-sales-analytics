from src.etl import run_pipeline

if __name__ == '__main__':
    _, report = run_pipeline()
    print('ETL pipeline completed:', report)
