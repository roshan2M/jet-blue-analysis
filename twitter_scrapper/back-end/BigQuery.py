from google.cloud import bigquery

class BigQuery(object):
    def __init__(self, dataset, table):
        self.client = bigquery.Client(project = "smart-inn-257104")
        self.table = self.client.get_table(self.client.dataset(dataset).table(table))
    
    def write_to_bigquery(self, rows):
        errors = self.client.insert_rows(self.table, rows)
        if len(errors) > 0:
            print(errors)