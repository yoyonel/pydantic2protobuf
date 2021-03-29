from typing import Optional

from pydantic import BaseModel, Field

from tests.models import IBaseModelForUTest


class GitInfo(BaseModel):
    branch_name: str = Field()
    committed_datetime: str = Field()
    commit_hex_sha: str = Field()


class StartupInfos(BaseModel):
    start_datetime: Optional[str] = None
    git_info: Optional[GitInfo] = None


class WebServerInfos(StartupInfos):
    state: str
    details: str


class GRPCInfo(BaseModel):
    host_and_port: str
    maximum_concurrent_rpc: int
    max_workers: int
    timeout: float


class WithNestedModelsResponse(IBaseModelForUTest):

    webserver: WebServerInfos = Field()
    grpc: GRPCInfo = Field()
    app: Optional[StartupInfos] = Field(None)

    @staticmethod
    def _get_expected_protobuf() -> str:
        return """message WithNestedModelsResponse {
    WebServerInfos webserver = 1;
    GRPCInfo grpc = 2;
    StartupInfos app = 3;
}
"""
