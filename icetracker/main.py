import icetracker


def get_status(process_list: list) -> str:
    i = icetracker.gen_index()
    p = icetracker.gen_procs(process_list)
    return icetracker.generate_full(i, p)


