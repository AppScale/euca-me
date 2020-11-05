from awacs.aws import Action, Policy, Principal, Statement
from troposphere import Parameter, Ref, Template
from troposphere.helpers.userdata import from_file
import troposphere.autoscaling as asc
import troposphere.ec2 as ec2
import troposphere.iam as iam

template = Template()

template.set_version("2010-09-09")
template.set_description("euca.me dns and http services")

availability_zone_1 = template.add_parameter(Parameter(
    "AvailabilityZone1",
    Description="1st EC2 availability zone to use",
    Type="String",
    Default="us-west-1a",
    ConstraintDescription="must be the name of an availability zone."
))

availability_zone_2 = template.add_parameter(Parameter(
    "AvailabilityZone2",
    Description="2nd EC2 availability zone to use",
    Type="String",
    Default="us-west-1c",
    ConstraintDescription="must be the name of an availability zone."
))

ssh_key_name = template.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair for instance SSH access",
    Type="String",
    ConstraintDescription="must be the name of an existing EC2 KeyPair."
))

instance_type = template.add_parameter(Parameter(
    "InstanceType",
    Description="EC2 instance type",
    Type="String",
    Default="t2.nano",
    AllowedValues=["t2.nano", "t2.micro", "t2.small", "t2.medium", "m1.small",
                   "m1.medium", "m1.large"],
    ConstraintDescription="must be a valid EC2 instance type."
))

image = template.add_parameter(Parameter(
    "Image",
    Description="EC2 image identifier",
    Type="String",
    Default="ami-bf5540df",
    AllowedPattern="[ae]mi-[0-9a-fA-F]{8}",
    ConstraintDescription="must be a valid EC2 image identifier."
))

vpc = template.add_resource(ec2.VPC(
    "Vpc",
    CidrBlock="10.0.0.0/16",
    EnableDnsSupport=True,
    EnableDnsHostnames=True,
    Tags=ec2.Tags(Name="euca.me")
))

subnet_1 = template.add_resource(ec2.Subnet(
    "Subnet1",
    VpcId=Ref(vpc),
    CidrBlock="10.0.0.0/24",
    AvailabilityZone=Ref(availability_zone_1),
    Tags=ec2.Tags(Name="euca.me")
))

subnet_2 = template.add_resource(ec2.Subnet(
    "Subnet2",
    VpcId=Ref(vpc),
    CidrBlock="10.0.1.0/24",
    AvailabilityZone=Ref(availability_zone_2),
    Tags=ec2.Tags(Name="euca.me")
))

internet_gateway = template.add_resource(ec2.InternetGateway(
    "InternetGateway",
    Tags=ec2.Tags(Name="euca.me")
))

vpc_gateway_attachment = template.add_resource(ec2.VPCGatewayAttachment(
    "GatewayToInternet",
    VpcId=Ref(vpc),
    InternetGatewayId=Ref(internet_gateway)
))

public_route_table = template.add_resource(ec2.RouteTable(
    "PublicRouteTable",
    VpcId=Ref(vpc),
    Tags=ec2.Tags(Name="euca.me")
))

public_route = template.add_resource(ec2.Route(
    "PublicRoute",
    DependsOn=["GatewayToInternet"],
    RouteTableId=Ref(public_route_table),
    DestinationCidrBlock="0.0.0.0/0",
    GatewayId=Ref(internet_gateway)

))

subnet_route_table_association_1 = template.add_resource(
    ec2.SubnetRouteTableAssociation(
        "SubnetRouteTableAssociation1",
        SubnetId=Ref(subnet_1),
        RouteTableId=Ref(public_route_table)
    )
)

subnet_route_table_association_2 = template.add_resource(
    ec2.SubnetRouteTableAssociation(
        "SubnetRouteTableAssociation2",
        SubnetId=Ref(subnet_2),
        RouteTableId=Ref(public_route_table)
    )
)

security_group = template.add_resource(ec2.SecurityGroup(
    "SecurityGroup",
    GroupDescription="SecurityGroup",
    VpcId=Ref(vpc),
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(IpProtocol="tcp", FromPort=53, ToPort=53,
                              CidrIp="0.0.0.0/0"),
        ec2.SecurityGroupRule(IpProtocol="udp", FromPort=53, ToPort=53,
                              CidrIp="0.0.0.0/0"),
        ec2.SecurityGroupRule(IpProtocol="tcp", FromPort=80, ToPort=80,
                              CidrIp="0.0.0.0/0")
    ],
    Tags=ec2.Tags(Name="euca.me")
))

role = template.add_resource(iam.Role(
    "Role",
    AssumeRolePolicyDocument=Policy(
        Version="2012-10-17",
        Statement=[
            Statement(
                Action=[Action("sts", "AssumeRole")],
                Effect="Allow",
                Principal=Principal("Service", ["ec2.amazonaws.com"]))
        ]
    ),
    Path="/",
    Policies=[
        iam.Policy(
            PolicyName="assign-public-address",
            PolicyDocument=Policy(
                Version="2012-10-17",
                Statement=[
                    Statement(
                        Action=[Action("ec2", "*Address*")],
                        Resource=["*"],
                        Effect="Allow"
                    )
                ]
            )
        )
    ]
))

instance_profile = template.add_resource(iam.InstanceProfile(
    "InstanceProfile",
    Path="/",
    Roles=[Ref(role)]
))

launch_configuration = template.add_resource(asc.LaunchConfiguration(
    "LaunchConfiguration",
    ImageId=Ref(image),
    SecurityGroups=[Ref(security_group)],
    InstanceMonitoring=False,
    IamInstanceProfile=Ref(instance_profile),
    InstanceType=Ref(instance_type),
    KeyName=Ref(ssh_key_name),
    UserData=from_file("out/cloud-config.yaml"),
    AssociatePublicIpAddress=True
))

autoscaling_group = template.add_resource(asc.AutoScalingGroup(
    "AutoScalingGroup",
    DependsOn=["PublicRoute"],
    AvailabilityZones=[Ref(availability_zone_1), Ref(availability_zone_2)],
    VPCZoneIdentifier=[Ref(subnet_1), Ref(subnet_2)],
    LaunchConfigurationName=Ref(launch_configuration),
    MinSize=0,
    MaxSize=1,
    DesiredCapacity=1,
    Tags=asc.Tags(Name="euca.me")
))

print(template.to_json())
