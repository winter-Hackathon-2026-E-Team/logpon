# JSON形式整形ファイル

# 初期画面表示
def serialize_initial(program_run, timer_runs):
    data = {}
    data['program_run'] = program_run
    data['timer_runs'] = list(timer_runs)
    return data