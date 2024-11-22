import os
import dotenv
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.compute import ComputeTarget, AmlCompute

dotenv.load_dotenv()

subscription_id = os.getenv("SUBSCRIPTION_ID")
tenant_id = os.getenv("TENANT_ID")
service_principal_id = os.getenv("SERVICE_PRINCIPAL_ID")
service_principal_password = os.getenv("SERVICE_PRINCIPAL_PASSWORD")

resource_group = "MLOpsCourseGroup"
workspace_name = "MLOpsCourse"
workspace_region = "germanywestcentral"


service_principal = ServicePrincipalAuthentication(
    tenant_id=tenant_id,
    service_principal_id=service_principal_id,
    service_principal_password=service_principal_password
)

ws = Workspace.create(
    name=workspace_name,
    subscription_id=subscription_id,
    resource_group=resource_group,
    location=workspace_region,
    auth=service_principal,
    create_resource_group=True,
    exist_ok=True
)

ws.get_details()
#ws.write_config()

amlcomputes = {
    "cpu-cluster": {
        "vm_size": "STANDARD_DS3_V2",
        "min_nodes": 0,
        "max_nodes": 1,
        "idle_seconds_before_scaledown": 240
    }
}

for ct_name in amlcomputes:
    if ct_name not in ws.compute_targets:
        compute_config = AmlCompute.provisioning_configuration(**amlcomputes[ct_name])
        ct = ComputeTarget.create(ws, ct_name, compute_config)
        ct.wait_for_completion(show_output=True)
        
ws.delete(delete_dependent_resources=True, no_wait=False)