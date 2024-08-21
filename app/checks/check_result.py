class CheckResult:
    def __init__(self, success: bool) -> None:
        self.success = success
        self.message = ""
        self.payloads = {}

    def add_message(self, message: str):
        self.message = message
        return self
    
    def add_payload(self, name: str, payload: any):
        self.payloads[name] = payload
        return self

    def passed(self) -> bool:
        return self.success
    
    def get_payload(self, name: str, default: any) -> any:
        return self.payloads.get(name, default)

    def message(self) -> str:
        return self.message
