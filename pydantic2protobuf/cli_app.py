import logging
from typing import Final

import click

from pydantic2protobuf.services.fastapi_to_proto import gen_proto_file_contents

app_name: Final[str] = "pydantic2proto"


@click.command()
def gen_proto_for_services():
    # from webserver.api.commands_with_grpc import router as commands_with_grpc_router
    # api = commands_with_grpc_router.api
    routes = []
    print(gen_proto_file_contents(routes))


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--log-level", default="WARN", help="set logging level")
def entry_point(log_level):
    logging.getLogger(app_name).setLevel(getattr(logging, log_level.upper()))


entry_point.add_command(gen_proto_for_services)

if __name__ == "__main__":
    entry_point()
