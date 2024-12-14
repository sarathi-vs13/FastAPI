from typing import Annotated,get_type_hints


def double(x: Annotated[int, (1,100)]) ->int:
    return x*2
    

result = double(5555)
print (result)