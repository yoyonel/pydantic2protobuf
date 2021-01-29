import logging

import click

from pydantic2protobuf.services.gen_protobuf import gen_protobuf_from_routes


@click.command()
def gen_proto_for_services():
    # from webserver.api.commands_with_grpc import router as commands_with_grpc_router
    # routes = commands_with_grpc_router.routes
    routes = []
    print(gen_protobuf_from_routes(routes))


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--log-level", default="WARN", help="set logging level")
def entry_point(log_level):
    logging.getLogger("talentminer").setLevel(getattr(logging, log_level.upper()))


entry_point.add_command(gen_proto_for_services)

if __name__ == "__main__":
    entry_point()
