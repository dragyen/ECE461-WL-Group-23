import time
from typing import Dict, Mapping, Tuple
from metrics import GradeResult

WEIGHTS: Dict[str,float]={
    
    "license":0.18,
    "ramp_up":0.15,
    "bus_factor":0.12,
    "performance_claims":0.1,
    "dataset_and_codescore":0.15,
    "dataset_quality":0.1,
    "code_quality":0.1,
    "size_score":0.1,
}

DEVICE_WEIGHTS = {
    "raspberry_pi": 0.30,
    "jetson_nano": 0.25,
    "aws_server": 0.25,
    "desktop_pc": 0.20,
}

#raspberry pi, jetson nano > aws, desktop. weights below
#rp: 0.3, jet nano: 0.25, desktop: 0.2, aws: 0.25

# We use this function to ensure our score will always be in a range from 0 to 1, inclusive.
def bounds(x: float, bottom: float = 0, top: float = 1) -> float:
    if x < bottom:
        return bottom
    if x > top:
        return top
    return x

# def compute(metrics: Mapping[str, float]) -> Tuple[float, int]:
#     startTime = time.perf_counter_ns()
    
#     net = float(0)
#     for key, w in WEIGHTS.items():
#         net += w * bounds(metrics.get(key,0.0))
        
#     net = bounds(net)
    
#     latency_ms = int((time.perf_counter_ns() - startTime)/(1000000))
    
#     return net, latency_ms


def compute(metrics: Mapping[str, float]) -> Tuple[float, int]:
    startTime = time.perf_counter_ns() 
  
    m=dict(metrics)
    m.setdefault("ramp_up_time", m.get("ramp_up"))
    m.setdefault("dataset_and_code_score", m.get("dataset_and_codescore"))
    
    sScore = m.get("size_score",0.0)
    if isinstance(sScore,Mapping):
        sScore = sum(DEVICE_WEIGHTS.get(k,0.0) * bounds(float(sScore.get(k,0.0) or 0.0))
                     for k in DEVICE_WEIGHTS)
        
    m["size_score", 0.0] = bounds(float(sScore))
    
    net = sum(w * bounds(float(m.get(k,0.0) or 0.0)) for k, w in WEIGHTS.items())
    net = bounds(net)
    
    latency_ms = int((time.perf_counter_ns()-startTime)/ 1,000,000)
    
    return net, latency_ms