class CheckResult:
    """A general result class that can be returned by any checking function.
    The idea is that messages and other data ("payloads") can easily be returned
    along with a success/failure boolean, and this data can be ignored or used
    at will by the caller without having to modify any code. 

    Checking functions can add as many payloads as they want by chaining together
    calls to add_payload, i.e.:
    return CheckResult(True).add_payload("foo", "bar").add_payload("blah", "blah")
    """

    def __init__(self, success: bool) -> None:
        self.success = success
        self._message = ""
        self.payloads = {}

    def add_message(self, message: str):
        """Add an optional message to the result.
        Normally this will be an error message in the case that success=False
        """
        self._message = str(message)
        return self
    
    def add_payload(self, name: str, payload: any):
        """Add a payload to the result. A payload can be of any type, and 
        can be used in any way that is relevant to the function's purpose.
        """
        self.payloads[name] = payload
        return self

    def passed(self) -> bool:
        return self.success
    
    def get_payload(self, name: str, default: any = None) -> any:
        return self.payloads.get(name, default)

    def message(self) -> str:
        return self._message
    
    def combine(self, other):
        """Makes it easier to chain results from multiple functions together
        by combining their payloads
        """
        self.payloads.update(other.payloads)
        return self
