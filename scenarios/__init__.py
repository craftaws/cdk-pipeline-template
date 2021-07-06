from aws_cdk import core
from artifacts import (
    infra,
    db,
)

class SampleScenarioStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        network = infra.Network(self, 'Network')
        db.Aurora(self, 'Aurora', bmt_vpc=network.vpc)
