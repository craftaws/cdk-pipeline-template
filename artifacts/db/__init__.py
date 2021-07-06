from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_rds as rds,
)

class Aurora(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, bmt_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        db_subnet_group = rds.SubnetGroup(self, 'Aurora',
            description='aurora subnet group',
            vpc=bmt_vpc,
            removal_policy=core.RemovalPolicy.DESTROY,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED)
        )

        db_security_group = ec2.SecurityGroup(self, 'aurora-sg',
            vpc=bmt_vpc
        )

        db_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4('10.100.0.0/16'),
            connection=ec2.Port(
                protocol=ec2.Protocol.TCP,
                string_representation="to allow from the vpc internal",
                from_port=3306,
                to_port=3306
            )
        )

        param_group = rds.ParameterGroup(self, 'bmt-aurora-param',
            engine=rds.DatabaseClusterEngine.AURORA_MYSQL
        )
        param_group.add_parameter("performance_schema", "1")

        rds.DatabaseCluster(self, 'bmt-aurora-cluster',
            engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_2_07_1),
            instance_props=rds.InstanceProps(
                vpc=bmt_vpc,
                instance_type=ec2.InstanceType.of(instance_class=ec2.InstanceClass.BURSTABLE3, instance_size=ec2.InstanceSize.MEDIUM),
                security_groups=[db_security_group]
            ),
            instances=1,
            subnet_group=db_subnet_group,
            parameter_group=param_group,
            removal_policy=core.RemovalPolicy.DESTROY
        )