from typing import Callable, Any
from mitmproxy.http import HTTPFlow
from utils.misc import is_fortnite_user_agent


def is_fortnite_request(
    func: Callable[[Any, HTTPFlow], Any]
) -> Callable[[Any, HTTPFlow], Any]:
    def wrapper(self: Any, flow: HTTPFlow):

        if not is_fortnite_user_agent(flow.request.headers.get("user-agent", "")):
            return

        return func(self, flow)

    return wrapper