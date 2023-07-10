import logging

from pydantic2protobuf.services.serializer.with_fstring import ProtoFileContentSerializerWithFString

try:
    from typing import Final
except ImportError:
    from typing import Optional as Final
import click

from pydantic2protobuf.services.fastapi_to_proto import gen_proto_file_contents

app_name: Final[str] = "pydantic2proto"


@click.command()
def gen_proto_for_services():
    # from webserver.api.commands_with_grpc import router as commands_with_grpc_router
    # api = commands_with_grpc_router.api
    routes = []
    serializer = ProtoFileContentSerializerWithFString()
    generated_proto = serializer(gen_proto_file_contents(routes))
    print(generated_proto)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option()
@click.option("--log-level", default="WARN", help="set logging level")
def entry_point(log_level):
    logging.getLogger(app_name).setLevel(getattr(logging, log_level.upper()))


entry_point.add_command(gen_proto_for_services)

if __name__ == "__main__":
    entry_point()
