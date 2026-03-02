from pydantic import BaseModel, ConfigDict
from typing import List

class MetricInfo(BaseModel):
    name: str

class MetricSetting(BaseModel):
    metric: MetricInfo
    activated: bool
    threshold: float
    includeReason: bool
    strictMode: bool
    sampleRate: float

class MetricCollection(BaseModel):
    id: str
    name: str
    multiTurn: bool
    metricsSettings: List[MetricSetting]

class ListMetricCollectionsResponse(BaseModel):
    metricCollections: List[MetricCollection]

