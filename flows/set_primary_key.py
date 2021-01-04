from dataflows import Flow, set_primary_key

def flow(parameters,*args):
    return Flow(
        set_primary_key(primary_key=parameters["primary-key"],
                    resources=parameters["resources"]
        )
    )

# Entrypoint for running the flow directly, without Datapackage Pipelines
if __name__ == '__main__':
    # Add a printer step and run the flow
    Flow(flow(), printer(num_rows=1, tablefmt='html')).process()