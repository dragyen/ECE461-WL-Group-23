import asyncio
import concurrent.futures

def bus_factor():
    return 1

def size():
    return 1

def ramp_up_time():
    return 1

def correctness():
    return 1

def license():
    return 1

def netscore():
    return 1

# async functions -- for api bound calculations
async def performance_claims():
    await asyncio.sleep(0.2)  # simulates api latency
    return 1

async def responsive_maintainer():
    await asyncio.sleep(0.4)
    return 1

async def code_quality():
    await asyncio.sleep(0.3)
    return 1

async def dataset_quality():
    await asyncio.sleep(0.6)
    return 1

async def dataset_code_score():
    await asyncio.sleep(0.7)
    return 1

# run tasks
def run_cpu_metrics():
    """Run CPU metrics in a process/thread pool."""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {
            "bus_factor": executor.submit(bus_factor),
            "size": executor.submit(size),
            "ramp_up_time": executor.submit(ramp_up_time),
            "correctness": executor.submit(correctness),
            "license": executor.submit(license),
            "netscore": executor.submit(netscore)
        }
        return {name: f.result() for name, f in futures.items()}

async def run_api_metrics():
    """Run async metrics concurrently."""
    tasks = {
        "performance_claims": asyncio.create_task(performance_claims()),
        "responsive_maintainer": asyncio.create_task(responsive_maintainer()),
        "code_quality": asyncio.create_task(code_quality()),
        "dataset_qualtiy": asyncio.create_task(dataset_quality()),
        "dataset_code_score": asyncio.create_task(dataset_code_score())
    }
    return {name: await task for name, task in tasks.items()}

async def run_all_metrics():
    # Run CPU (executor) + API (async) concurrently
    loop = asyncio.get_running_loop()
    cpu_future = loop.run_in_executor(None, run_cpu_metrics)
    api_future = asyncio.create_task(run_api_metrics())

    cpu_results, api_results = await asyncio.gather(cpu_future, api_future)
    return {**cpu_results, **api_results}

if __name__ == "__main__":
    results = asyncio.run(run_all_metrics())
    print("All metric results:", results)
