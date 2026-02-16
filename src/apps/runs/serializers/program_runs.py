# JSON形式整形ファイル

# 既存programsの整形
def serialize_exist_programs(programs):
    data = {}
    data['programs'] = list(programs)
    return data

# 既存runsの整形
def serialize_exist_runs(program_run, timer_runs):
    data = {}
    data['program_run'] = program_run
    data['timer_runs'] = list(timer_runs)
    return data