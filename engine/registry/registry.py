import engine.registry.runtimeconfig as runtime_config
import engine.registry.gameinfo as game_info
import engine.registry.gamecapacities as game_capacities
import time

def load():
    start_time = time.perf_counter()
    runtime_config.load()
    game_info.load()
    game_capacities.load()
    print(f"Registry loaded in {time.perf_counter()-start_time}")