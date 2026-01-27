from feast import Entity
from feast.types import String

container = Entity(
    name="container",
    join_keys=["container_id"],
    value_type=String,
    description="Unique container ID for inspection and shipment",
)
