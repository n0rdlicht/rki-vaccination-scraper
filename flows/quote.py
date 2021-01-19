from dataflows import Flow, delete_fields, add_computed_field, conditional
import math

def tryconvert(value, default, *types):
    for t in types:
        try:
            return t(value)
        except (ValueError, TypeError):
            continue
    return default

def field_exists(field_name):
    def func(dp):
        return all(field_name == f.name for f in dp.resources[0].schema.fields)
    return func

def flow(parameters, *args):
    return Flow(
        conditional(
            field_exists('quote'), Flow(
                delete_fields(["quote"],resources=parameters["resources"])
            )
        ),
        add_computed_field(target=dict(name='quote',type='number'),
                            operation=lambda row: (row["key"]=="sum") and round(tryconvert(row["value"],0,int)/math.floor(tryconvert(row["population"],100,int)/100),2) or None,
                            resources=parameters["resources"]
        )
    )

# Entrypoint for running the flow directly, without Datapackage Pipelines
if __name__ == '__main__':
    # Add a printer step and run the flow
    Flow(flow, printer(num_rows=1, tablefmt='html')).process()