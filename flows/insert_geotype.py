from dataflows import Flow, add_computed_field

def flow(*args):
    return Flow(
        add_computed_field(target=dict(name='geotype',type='string',constraints=dict(enum=["state","nation"])),
                            operation=lambda row: (row['geo'] == 'Germany') and 'nation' or 'state',
                            resources='de-vaccinations-current'
        )
    )

# Entrypoint for running the flow directly, without Datapackage Pipelines
if __name__ == '__main__':
    # Add a printer step and run the flow
    Flow(flow(), printer(num_rows=1, tablefmt='html')).process()