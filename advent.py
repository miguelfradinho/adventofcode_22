import sol_snake
from utils import get_file


if __name__ == "__main__":
    fun_prefix = "day_"
    fun_names = [f for f in dir(sol_snake) if f.startswith(fun_prefix)]
    STOP = 8
    STOP_AT = f"{fun_prefix}{STOP+1}"

    for i in fun_names:
        if i == STOP_AT:
            break
        fun = getattr(sol_snake, i)
        file_obj = get_file(i)
        print(f"{i} - {fun(file_obj)}")
