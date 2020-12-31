from dataflows import Flow, add_computed_field
from datetime import datetime, timedelta

def flow(parameters, *args):
    return Flow(
        add_computed_field(target=dict(name='date',type='date'),
                            operation=lambda row: datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d'),
                            resources=parameters["resources"]
        )
    )

# Entrypoint for running the flow directly, without Datapackage Pipelines
if __name__ == '__main__':
    # Add a printer step and run the flow
    Flow(flow(), printer(num_rows=1, tablefmt='html')).process()